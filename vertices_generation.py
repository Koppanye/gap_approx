import numpy as np

from instance import InstanceRestrictedAssignment
from instances_template import pick_one_instance
import subprocess

if __name__ == "__main__":
    filename = "model.lp"

    input_matrix = "koppany_2025_short"

    n_jobs, n_machines, M = pick_one_instance(input_matrix)

    instance = InstanceRestrictedAssignment(n_jobs, n_machines, generate=False, M = M)
    T = instance.opt_LP(verbose=False)
    instance.get_A_b_eq(T, filename=filename)
    #T_IP = instance.opt_IP(verbose=False)

    # Write polimake script
    """
    $f = lp2poly('model.lp');
    $p = new Polytope<Rational>($f);
    print $p -> VERTICES;
    """
    F = open("to_run.txt", "w+")

    F.write("use application \"polytope\";\n")
    F.write("my $f = lp2poly('" + filename + "');\n")
    F.write("my $p = new Polytope<Rational>($f);\n")
    F.write("print $p -> VERTICES;\n")
    F.close()

    subprocess.run("polymake --script to_run.txt > vertices_eq.txt", shell=True)