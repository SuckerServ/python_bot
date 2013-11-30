server = {
	'ping': lambda server_write, **_: server_write('code:sendmsg("pong!")'),
	'players': lambda server_write, **_: server_write('\
		code:local msg = "" \
			for p in server.gplayers() do \
				if server.player_priv_code(p.cn) >= server.PRIV_ADMIN then \
					msg = msg .. irc_color_orange(string.format("%s(%d)", p:name(), p.cn)) \
				elseif server.player_priv_code(p.cn) >= server.PRIV_MASTER then \
					msg = msg .. irc_color_green(string.format("%s(%d)", p:name(), p.cn)) \
				else \
					msg = msg .. string.format("%s(%d) ", p:name(), p.cn) \
				end \
			end \
			if msg == "" then\
				sendmsg("no players connected")\
			else\
				sendmsg(msg)\
			end\
		'),
	'restart': lambda server_write, **_: server_write('code:sendmsg("restarting server..."); server.restart_now()'),
	'uptime': lambda server_write, **_: server_write('code:sendmsg("Uptime: " .. server.format_duration(server.uptime))'),
}

def f(server_write, args, nickname, **_):
    server_write('''code:\
	server.msg("\f3>>> \f1REMOTE ADMIN (%s)\ff: %s");\
	sendmsg("REMOTE ADMIN (%s): %s")\
	''' % (nickname, args, nickname, args))
	
server['say'] = f


def f(server_write, args, nickname, **_):
    server_write('''\
			code:local cn = tonumber('%s')\
			if server.valid_cn(cn) then\
				server.kick(cn, 9999, "%s", "kicked by a remote admin.")\
			else\
				sendmsg("player not found")\
			end\
			\
			\
			''' % (args.split()[0],args.split()[1]))
server['kick'] = f

def f(server_write, args, **_):
    server_write('''\
			code:local cn = tonumber('%s')\
			if server.valid_cn(cn) then\
				sendmsg("Name: "..server.player_name(cn).." Frags: "..server.player_frags(cn).." Deaths: "..server.player_deaths(cn).."  Accuracy: "..server.player_accuracy(cn)..string.char(37).." Ping: "..server.player_ping(cn).." Country: "..geoip.ip_to_country(server.player_ip(cn)))\
			else\
				sendmsg("player not found")\
			end\
			\
			\
			''' % args)
server['stats'] = f

def f(server_write, args, **_):
    server_write('''\
			code:local cn = tonumber('%s'); local min = tonumber('%s');\
			if server.valid_cn(cn) then\
				server.mute(cn, min)\
				sendmsg("muted " .. server.player_name(cn) .. " for " .. min .. " minutes")
			else\
				sendmsg("player not found")\
			end\
			\
			\
			''' % (args.split()[0],args.split()[1]))
server['mute'] = f

def f(server_write, args, **_):
    server_write('''\
			code:local cn = tonumber('%s');\
			if server.valid_cn(cn) then\
				server.unmute(cn)\
				sendmsg("unmuted " .. server.player_name(cn))
			else\
				sendmsg("player not found")\
			end\
			\
			\
			''' % args)
server['unmute'] = f



def f(server_write, args, **_):
    server_write('''\
			code:local cn = tonumber('%s');\
			if server.valid_cn(cn) then\
				server.disconnect(cn, 10, "disconnect by a admin")\
			else\
				sendmsg("player not found")\
			end\
			\
			\
			''' % args)
server['disconnect'] = f


def f(server_write, args, **_):
    server_write('''\
			code:local cn = tonumber('%s');\
			if server.valid_cn(cn) then\
				server.spec(cn)\
			else\
				sendmsg("player not found")\
			end\
			\
			\
			''' % args)
server['spec'] = f

def f(server_write, args, **_):
	server_write('''\
			code:local cn = tonumber('%s');\
			if server.valid_cn(cn) then\
				server.slay(cn)\
				sendmsg("player slayed")\
			else\
				sendmsg("player not found")\
			end\
			\
			\
			''' % args)
server['slay'] = f
			

def f(server_write, args, **_):
    server_write('''\
			code:local cn = tonumber('%s');\
			if server.valid_cn(cn) then\
				server.unspec(cn)\
			else\
				sendmsg("player not found")\
			end\
			\
			\
			''' % args)
server['unspec'] = f

def f(server_write, args, **_):
    server_write('''\
			code:server.pausegame(1)\
			''')
server['pause'] = f

def f(server_write, args, **_):
    server_write('''\
			code:server.pausegame(false)\
			''')
server['resume'] = f

def f(server_write, args, **_):
	server_write('''\
			code:server.specall(true)\
			''')
server['specall'] = f

def f(server_write, args, **_):
	server_write('''\
			code:server.unspecall(true)\
			''')
server['unspecall'] = f

def f(server_write, args, **_):
	server_write('''\
			code:server.recorddemo\
			''')
server['recorddemo'] = f

def f(server_write, args, **_):
	server_write('''\
			code:server.stopdemo\
			''')
server['stopdemo'] = f

def f(server_write, args, **_):
    server_write('''\
			code:local cn = tonumber('%s');\
			if server.valid_cn(cn) then\
				sendmsg("IP: "..server.player_ip(cn))\
			else\
				sendmsg("player not found")\
			end\
			\
			\
			''' % args)
server['ip'] = f

def f(server_write, args, **_):
    server_write('''\
			code:\
				server.changemap("%s")\
			''' % args)
server['map'] = f

def f(server_write, args, **_):
    server_write('''\
			code:\
				server.changetime(tonumber('%s')*1000*60)\
			''' % args)
server['changetime'] = f

def f(server_write, args, **_):
    server_write('''\
			code:server.reloadscripts(1)\
			''')
server['reload'] = f		

def f(server_write, args, **_):
    server_write('''\
                        code:server.clearbans()\
                        sendmsg(cube2irc_colors(server.clearbans_message))\
                        ''')
server['clearbans'] = f

def f(server_write, args, **_):
	server_write('''\
		code:sendmsg(\
			string.format(\
				irc_color_green("Gamemode:") .." %s " .. irc_color_grey("|") .. irc_color_green("Map:") .. " %s " .. irc_color_grey("|") .. irc_color_green("Players:") .. " %s " .. irc_color_grey("|") .. irc_color_green("Time left:") .. " %s min " .. irc_color_grey("|") .. irc_color_green("Mastermode:") .. " %s", \
				irc_color_blue(server.gamemode), irc_color_blue(server.map), irc_color_blue(server.playercount), irc_color_blue(server.timeleft), irc_color_blue(server.mastermode)\
			)\
		)\
	''')
server['info'] = f
