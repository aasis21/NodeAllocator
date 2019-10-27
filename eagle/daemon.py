"""Generic linux daemon base class for python 3.x."""

import sys
import os
import time
import atexit
import signal
import sqlite3
import subprocess
import psutil

class Daemon:
	"""A generic daemon class.
	Usage: subclass the daemon class and override the run() method.
	"""

	def  __init__(self, pidfile, stdout='/dev/null', stderr='/dev/null', stdin='/dev/null'):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile

	def daemonize(self):
		"""Deamonize class. UNIX double fork mechanism."""
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit first parent
				sys.exit(0) 
		except OSError as err: 
			sys.stderr.write('fork #1 failed: {0}\n'.format(err))
			sys.exit(1)
	
		# decouple from parent environment
		os.chdir('/') 
		os.setsid() 
		os.umask(0) 
	
		# do second fork
		try: 
			pid = os.fork() 
			if pid > 0:

				# exit from second parent
				sys.exit(0) 
		except OSError as err: 
			sys.stderr.write('fork #2 failed: {0}\n'.format(err))
			sys.exit(1) 

		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = open(self.stdin, 'r')
		so = open(self.stdout, 'a+')
		se = open(self.stderr, 'a+')
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
	
		# write pidfile
		atexit.register(self.delpid)

		pid = str(os.getpid())
		with open(self.pidfile,'w+') as f:
			f.write(pid + '\n')

	
	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		"""Start the daemon."""

		# Check for a pidfile to see if the daemon already runs
		try:
			with open(self.pidfile,'r') as pf:
				pid = int(pf.read().strip())
			if psutil.pid_exists(pid):
				pass
			else:
				pid = None
		except:
			pid = None
	
		if pid:
			message = "Daemon already Running !!!\n"
			sys.stderr.write(message.format(self.pidfile))
			sys.exit(1)
		
		# Start the daemon
		self.daemonize()
		self.run()

	def stop(self):
		"""Stop the daemon."""

		# Get the pid from the pidfile
		try:
			with open(self.pidfile,'r') as pf:
				pid = int(pf.read().strip())
		except IOError:
			pid = None
	
		if not pid:
			message = "Daemon not Running !!!\n"
			sys.stderr.write(message.format(self.pidfile))
			return # not an error in a restart

		# Try killing the daemon process	
		try:
			while 1:
				os.kill(pid, signal.SIGTERM)
				time.sleep(0.1)
		except OSError as err:
			e = str(err.args)
			if e.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print (str(err.args))
				sys.exit(1)

	def restart(self):
		"""Restart the daemon."""
		self.stop()
		self.start()

	def run(self):
		"""You should override this method when you subclass Daemon.
		
		It will be called after the process has been daemonized by 
		start() or restart()."""
	
	def setupDB(self, dbfile):
		con = sqlite3.connect(dbfile)
		cur = con.cursor()

		print("Setting DB Tables ::: ", end = " ")

		latency_sql = """
		CREATE TABLE latency (
			hostA INTEGER NOT NULL,
			hostB INTEGER NOT NULL,
			latency INTEGER NOT NULL,
			time TIMESTAMP DEFAULT  (strftime('%s','now')),
			PRIMARY KEY (hostA, hostB)
		)"""

		try:
			cur.execute(latency_sql)
		except:
			print("LT Table : UP, ", end = " ")

		latency_monitor_sql = """
		CREATE TABLE latency_monitor (
			id INTEGER PRIMARY KEY,
			hostA INTEGER NOT NULL,
			hostB INTEGER NOT NULL,
			latency INTEGER NOT NULL,
			time TIMESTAMP DEFAULT  (strftime('%s','now'))
		)"""
		try:
			cur.execute(latency_monitor_sql)
		except:
			print("LT M Table : UP, ", end = " ")

		bw_sql = """
		CREATE TABLE bw (
			hostA INTEGER NOT NULL,
			hostB INTEGER NOT NULL,
			bw INTEGER NOT NULL,
			time TIMESTAMP DEFAULT  (strftime('%s','now')),
			PRIMARY KEY (hostA, hostB)
		)"""

		try:
			cur.execute(bw_sql)
		except:
			print("BW Table : UP, ", end = " ")

		bw_monitor_sql = """
		CREATE TABLE bw_monitor (
			id INTEGER PRIMARY KEY,
			hostA INTEGER NOT NULL,
			hostB INTEGER NOT NULL,
			bw INTEGER NOT NULL,
			time TIMESTAMP DEFAULT  (strftime('%s','now'))
		)"""
		try:
			cur.execute(bw_monitor_sql)
		except:
			print("BW M Table : UP, ", end = " ")

		

		node_sql = """
		CREATE TABLE node (
			node TEXT NOT NULL PRIMARY KEY,
			cpucount INTEGER NOT NULL,
			corecount INTEGER NOT NULL,

			cpufreqmin INTEGER NOT NULL,
			cpufreqcurrent INTEGER NOT NULL,
			cpufreqmax INTEGER NOT NULL,

			load_1 REAL NOT NULL,
			load_5 REAL NOT NULL,
			load_15 REAL NOT NULL,
			
			band_10 REAL NOT NULL,
			band_50 REAL NOT NULL,
			band_150 REAL NOT NULL,
			
			util_10 REAL NOT NULL,
			util_50 REAL NOT NULL,
			util_150 REAL NOT NULL,
			
			memory INTEGER NOT NULL,
			memory_10 INTEGER NOT NULL,
			memory_50 INTEGER NOT NULL,
			memory_150 INTEGER NOT NULL,

			nodeusers INTEGER NOT NULL,

			time TIMESTAMP DEFAULT  (strftime('%s','now'))
		)"""

		try:
			cur.execute(node_sql)
		except:
			print("NODE Table : UP, ", end = " ")


		node_monitor_sql = """
		CREATE TABLE node_monitor (
			id INTEGER PRIMARY KEY,
			node TEXT NOT NULL,
			cpucount INTEGER NOT NULL,
			corecount INTEGER NOT NULL,

			cpufreqmin INTEGER NOT NULL,
			cpufreqcurrent INTEGER NOT NULL,
			cpufreqmax INTEGER NOT NULL,

			load_1 REAL NOT NULL,
			load_5 REAL NOT NULL,
			load_15 REAL NOT NULL,
			
			band_10 REAL NOT NULL,
			band_50 REAL NOT NULL,
			band_150 REAL NOT NULL,
			
			util_10 REAL NOT NULL,
			util_50 REAL NOT NULL,
			util_150 REAL NOT NULL,
			
			memory INTEGER NOT NULL,
			memory_10 INTEGER NOT NULL,
			memory_50 INTEGER NOT NULL,
			memory_150 INTEGER NOT NULL,

			nodeusers INTEGER NOT NULL,
			
			time TIMESTAMP DEFAULT  (strftime('%s','now'))
		)"""

		try:
			cur.execute(node_monitor_sql)
		except:
			print("Node M Table : UP, ", end = " ")
		
		print(" ::: DONE")


		con.close()