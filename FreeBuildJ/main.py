import sys
import os,os.path
from net.cemetech.sfgp.freebuild.drivers import Drivers
from java.lang import System


def is_package_dir(parent,path):
	rpath = os.path.join(parent,path)
	return path if (os.path.exists(rpath) and \
					os.path.isdir(rpath) and \
					os.path.exists(os.path.join(rpath,"__init__.py"))) else ""

def is_python_module(path):
	lp = len(path)
	if (lp > 3 and path[-3:] in [".py",".so"]):
		ret = path[:-3]
	elif (lp > 4 and path[-4:] in [".pyc",".pyd",".pyo"]):
		ret = path[:-4]
	else:
		ret = ""
	return ret

def not_excluded_name(path):
	return path not in [".","..","__init__.py","__init__.pyc"]

def determine_package(path):
	if os.path.isdir(path):
		return list(set(is_package_dir(path,fname) or is_python_module(fname) for fname in os.listdir(path) if (is_package_dir(path,fname) or is_python_module(fname)) and not_excluded_name(fname)))
	else:
		raise ValueError("'%s' is not a valid directory" % (path))

# Note the differing default semantics as compared to __import__
def export_symbols(module_name,globals,locals,fromlist,level=0):
	temp_module = __import__(module_name,globals,locals,fromlist,level)
	for symbol in fromlist:
		globals[symbol] = temp_module.__dict__[symbol]


def main(*argv):
	print "//---------------------------------------------"
	print
	print "Parsing startup arguments"
	if not argv or "--dedicated" not in argv[1:]:
		Drivers.clearMainDriver()
		GFXDriver = Drivers.getNamedDriver("GFXDriver")
		driver = GFXDriver()
		
		# Here we should explicitly load a settings file
		import json
		with open("data/prefs/defaults.json",'r') as defaults:
			for k,v in json.load(defaults).items(): driver.settings()[k] = v
		with open("data/prefs/prefs.json",'r') as prefs:
			for k,v in json.load(prefs).items(): driver.settings()[k] = v
		Drivers.setMainDriver(driver)
		
		from net.cemetech.sfgp.ldraw import LDManager
		LDManager.init()
		LDManager.parseModel("car.dat")
		print driver.settings
	else:
		print "Dedicated server requested"
		print "But no such driver exists"
	print 
	print "---------------------------------------------//"
	print

if __name__ == "__main__":
	main(*sys.argv)