"""Main entry point for the backend application."""

from agents.intake_agent import IntakeAgent
from agents.supervisor_agent import SupervisorAgent


def main():
    """Main entry point."""
    print("RailsEVA AI Backend Starting...")
    
    # Initialize agents
    intake_agent = IntakeAgent()
    supervisor = SupervisorAgent()
    
    # Start application
    pass


if __name__ == "__main__":
    main()
