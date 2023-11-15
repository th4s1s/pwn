import angr
p = angr.Project('./lucid')
state = p.factory.entry_state()
simgr = p.factory.simulation_manager(state)
simgr.explore(find=0x8049671, avoid=0x80496d4)
for i in range(3):
    print(simgr.found[0].posix.dumps(i))