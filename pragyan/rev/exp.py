import angr
p = angr.Project('./reverse_me')
state = p.factory.entry_state()
simgr = p.factory.simulation_manager(state)
simgr.explore(find=0x4015e2, avoid=0x4015f3)
for i in range(3):
    print(simgr.found[0].posix.dumps(i))