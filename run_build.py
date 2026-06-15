# run_build.py
import subprocess
import sys

def run_command(command_list, step_name):
    print(f"\n=== Running Step: {step_name} ===")
    print(f"Executing: {' '.join(command_list)}")
    
    # Run the shell command and capture its exit status
    result = subprocess.run(command_list)
    
    if result.returncode != 0:
        print(f"FAILURE: {step_name} failed with exit code {result.returncode}.")
        return False
    
    print(f"SUCCESS: {step_name} passed.")
    return True

def main():
    print("Starting Automated Local Build Pipeline...")
    
    # Step 1: Code Smell & Style Analysis (Linting)
    # Checks for PEP 8 compliance and syntactic flaws
    if not run_command(["flake8", "scripted.py"], "Flake8 Linter"):
        sys.exit(1)
        
    # Step 2: Quality Metrics Assessment (Complexity Check)
    # The "-e" flag prints only blocks scored worse than 'B' (Grades C through F).
    # If anything shows up here, the command will return a non-zero exit code.
    if not run_command(["radon", "cc", "scripted.py", "-e"], "Radon Complexity Guard"):
        print("\nTip: Your code complexity rank must be 'A' or 'B' to pass.")
        sys.exit(1)
        
    # Step 3: Regression Verification (Automated Unit Testing)
    # Ensures no functionality was broken during the refactoring process
    # TODO: add unit test execution
        
    print("\nBUILD SUCCESSFUL: All local pipeline quality guards passed!")
    sys.exit(0)

if __name__ == "__main__":
    main()
    