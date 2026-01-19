"""
Job & Work Commands Cog
/work, /work list, /work info
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.economy import get_player, player_exists, get_player_stats_summary
from utils.jobs import work_job, get_available_jobs, get_job_info, get_job_list

class JobCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="work", description="Work a job to earn money")
    @app_commands.describe(job="Job ID to work")
    async def work(self, interaction: discord.Interaction, job: str = None):
        """Work a job"""
        user_id = interaction.user.id
        
        if not player_exists(user_id):
            embed = discord.Embed(
                title="❌ No Account",
                description="Use `/setup` to create an account!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        player = get_player(user_id)
        
        if not job:
            # Show available jobs
            available = get_available_jobs(player["level"])
            if not available:
                embed = discord.Embed(
                    title="❌ No Jobs Available",
                    description="Level up to unlock more jobs!",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed)
                return
            
            embed = discord.Embed(
                title="💼 Available Jobs",
                description=f"You are level {player['level']}\n\nUse `/work [job_id]` to work",
                color=discord.Color.blurple()
            )
            embed.description += "\n\n" + get_job_list(player["level"])
            embed.set_footer(text="Example: /work street_vendor")
            await interaction.response.send_message(embed=embed)
            return
        
        # Work the job
        result = work_job(user_id, job.lower())
        
        if "error" in result:
            embed = discord.Embed(
                title="❌ Error",
                description=result["error"],
                color=discord.Color.red()
            )
            if "remaining_seconds" in result:
                minutes = result["remaining_seconds"] / 60
                embed.add_field(name="Cooldown", value=f"{minutes:.1f} minutes remaining")
            await interaction.response.send_message(embed=embed)
            return
        
        # Success!
        job_info = get_job_info(job.lower())
        embed = discord.Embed(
            title=f"{job_info['emoji']} {job_info['name']}",
            description=result["message"],
            color=discord.Color.green() if result["success"] else discord.Color.red()
        )
        
        if result["success"]:
            embed.add_field(name="Earnings", value=f"💰 ${result['payout']:,}")
            embed.add_field(name="XP", value=f"📊 +{result['xp']}")
            if result.get("critical"):
                embed.add_field(name="⚡", value="CRITICAL SUCCESS!")
            
            updated_player = get_player(user_id)
            embed.add_field(name="Job Streak", value=f"🔥 {updated_player.get('job_streak', 0)}")
        else:
            embed.add_field(name="Lost", value=f"❌ ${result['lost']:,}")
            embed.add_field(name="XP", value=f"📊 +{result['xp']}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="work_list", description="See available jobs for your level")
    async def work_list(self, interaction: discord.Interaction):
        """List available jobs"""
        user_id = interaction.user.id
        
        if not player_exists(user_id):
            embed = discord.Embed(
                title="❌ No Account",
                description="Use `/setup` to create an account!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        player = get_player(user_id)
        
        embed = discord.Embed(
            title=f"💼 Available Jobs (Level {player['level']})",
            description="Use `/work [job_id]` to work\n\n" + get_job_list(player["level"]),
            color=discord.Color.blurple()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="work_info", description="Get detailed info about a job")
    @app_commands.describe(job="Job ID")
    async def work_info(self, interaction: discord.Interaction, job: str):
        """Get job info"""
        
        job_info = get_job_info(job.lower())
        
        if not job_info:
            embed = discord.Embed(
                title="❌ Job Not Found",
                description=f"Job '{job}' does not exist",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        embed = discord.Embed(
            title=f"{job_info['emoji']} {job_info['name']}",
            description=job_info['description'],
            color=discord.Color.blurple()
        )
        
        embed.add_field(name="Tier", value=job_info['tier'], inline=True)
        embed.add_field(name="Min Level", value=job_info['min_level'], inline=True)
        embed.add_field(name="Cooldown", value=f"{job_info['cooldown']}s", inline=True)
        
        embed.add_field(name="Payout", value=f"${job_info['payout_min']:,} - ${job_info['payout_max']:,}", inline=False)
        
        # Stat scaling
        scaling_text = ""
        for stat, weight in job_info['stat_scaling'].items():
            scaling_text += f"**{stat.title()}**: {weight*100:.0f}%\n"
        embed.add_field(name="Stat Scaling", value=scaling_text, inline=False)
        
        embed.add_field(name="Base Success Rate", value=f"{job_info['base_success_rate']*100:.0f}%", inline=False)
        
        await interaction.response.send_message(embed=embed)

# Setup function
async def setup(bot):
    await bot.add_cog(JobCommands(bot))
