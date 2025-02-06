import UVSim

def main():
    sim = UVSim.UVSim()
    sim.load_program()
    print(sim.memory)
    sim.execute()

if __name__ == '__main__':
    main()
