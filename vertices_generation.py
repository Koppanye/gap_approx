import numpy as np

from instance import InstanceRestrictedAssignment
from instances_template import pick_one_instance
import subprocess

if __name__ == "__main__":
    filename_eq = "model_eq.lp"
    filename_ineq = "model_ineq.lp"

    input_matrix = "koppany_2025_short"

    n_jobs, n_machines, M = pick_one_instance(input_matrix)

    instance = InstanceRestrictedAssignment(n_jobs, n_machines, generate=False, M = M)
    T = instance.opt_LP(verbose=False)
    instance.get_A_b_eq(T, filename=filename_eq)
    instance.get_A_b(T, filename=filename_ineq)
    ##x, T_IP = instance.opt_IP(verbose=False)

    #print("The integrality gap is ", T_IP / T)

    # Write polymake script
    """
    $f = lp2poly('model.lp');
    $p = new Polytope<Rational>($f);
    print $p -> VERTICES;
    """
    # With equalities
    F = open("to_run.txt", "w+")

    F.write("use application \"polytope\";\n")
    F.write("my $f = lp2poly('" + filename_eq + "');\n")
    F.write("my $p = new Polytope<Rational>($f);\n")
    F.write("print $p -> VERTICES;\n")
    F.close()

    subprocess.run("polymake --script to_run.txt > ./vertices/vertices_{}_eq.txt".format(input_matrix), shell=True)

    # With inequalities
    F = open("to_run.txt", "w+")

    F.write("use application \"polytope\";\n")
    F.write("my $f = lp2poly('" + filename_ineq + "');\n")
    F.write("my $p = new Polytope<Rational>($f);\n")
    F.write("print $p -> VERTICES;\n")
    F.close()

    subprocess.run("polymake --script to_run.txt > ./vertices/vertices_{}_ineq.txt".format(input_matrix), shell=True)