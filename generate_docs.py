"""
Script to generate documentation assets and update project documentation.
"""
import os
import logging
from pathlib import Path
from inventory.documentation_generator import DocumentationGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Generate documentation assets and update markdown."""
    try:
        logger.info("Starting documentation generation process")

        # Initialize documentation generator
        doc_gen = DocumentationGenerator()

        # Generate assets
        logger.info("Generating documentation assets...")
        assets = doc_gen.generate_documentation_assets()

        # Print summary
        print("\nGenerated assets:")
        for asset_type, paths in assets.items():
            print(f"\n{asset_type.title()}:")
            for path in paths:
                print(f"- {path}")

        # Check if all sections were generated
        missing_sections = []
        if not assets['diagrams']:
            missing_sections.append("System Architecture Diagram")
        if not assets['screenshots']:
            missing_sections.append("UI Screenshots")

        if missing_sections:
            logger.warning("Some sections were not generated:")
            for section in missing_sections:
                logger.warning(f"- {section}")
        else:
            logger.info("All documentation assets were generated successfully!")

        # Verify output directory
        output_dir = Path("docs/assets")
        if output_dir.exists():
            num_files = len(list(output_dir.glob('*')))
            logger.info(f"Total files in output directory: {num_files}")

    except Exception as e:
        logger.error(f"Error during documentation generation: {str(e)}")
        raise

if __name__ == "__main__":
    main()