"""Demonstrates molecular dynamics with constant energy."""
from asap3 import Trajectory
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units

def calcenergy(a):
	epot = a.get_potential_energy() / len(a)
	ekin = a.get_kinetic_energy() / len(a)
	calcenergy = (epot, ekin, ekin / (1.5 * units.kB), epot + ekin)
	return calcenergy

# Use Asap for a huge performance increase if it is installed
def run_md():
	use_asap = True
	if use_asap:
    		from asap3 import EMT
    		size = 10
	else:
    		from ase.calculators.emt import EMT
    		size = 3
    
# Set up a crystal
	atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                          symbol="Cu",
                          size=(size, size, size),
                          pbc=True)

# Describe the interatomic interactions with the Effective Medium Theory
	atoms.calc = EMT()

# Set the momenta corresponding to T=300K
	MaxwellBoltzmannDistribution(atoms, 300 * units.kB)

# We want to run MD with constant energy using the VelocityVerlet algorithm.
	dyn = VelocityVerlet(atoms, 5 * units.fs)  # 10 fs time step.
	traj = Trajectory('cu.traj','w', atoms)
	dyn.attach(traj.write, interval=10)

	def printenergy(a):  # store a reference to atoms in the definition.
	#Function to print the potential, kinetic and total energy."""
    		print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
        	'Etot = %.3feV' % calcenergy(a))

# Now run the dynamics
	printenergy(atoms)
	for i in range(10):
		dyn.run(10)
		printenergy(atoms)

if  __name__ == "__main__":
	run_md()
