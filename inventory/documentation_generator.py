"""
Documentation generator module for the Inventory Management System.
Handles automated generation of screenshots and diagrams.
"""
import os
import logging
from datetime import datetime
from typing import List, Optional, Dict
from pathlib import Path
import json
from contextlib import contextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DocumentationGenerator:
    """
    Handles generation of documentation assets including screenshots and diagrams.
    """

    @contextmanager
    def get_chrome_driver(self):
        """Get configured Chrome driver for Replit environment."""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service

        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--window-size=1920,1080')

        # Create Service object with specific binary path for Replit
        service = Service(executable_path='/nix/store/zi4f80l169xlmivz8vja8wlphq74qqk0-chromium-125.0.6422.141/bin/chromium')

        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            yield driver
        finally:
            if 'driver' in locals():
                driver.quit()
                logger.info("Closed Chrome driver")

    def __init__(self, output_dir: str = "docs/assets"):
        """
        Initialize the documentation generator.

        Args:
            output_dir (str): Directory to store generated assets
        """
        self.output_dir = output_dir
        self._ensure_dependencies()
        self._setup_directories()

    def _ensure_dependencies(self) -> None:
        """Verify that required dependencies are available."""
        try:
            import graphviz
            logger.info("Graphviz package is available")
        except ImportError:
            logger.error("Graphviz package is not installed")
            raise ImportError("Please install graphviz package")

        try:
            from selenium import webdriver
            logger.info("Selenium package is available")

            # Verify Chrome binary
            chrome_path = '/nix/store/zi4f80l169xlmivz8vja8wlphq74qqk0-chromium-125.0.6422.141/bin/chromium'
            if not os.path.exists(chrome_path):
                raise ImportError("Chromium binary not found")
            logger.info("Chromium binary found")

        except ImportError as e:
            logger.error(f"Selenium or Chrome setup error: {str(e)}")
            raise

    def _setup_directories(self) -> None:
        """Create necessary directories for documentation assets."""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created output directory: {self.output_dir}")

    def generate_system_architecture_diagram(self) -> str:
        """
        Generate a system architecture diagram using Graphviz.

        Returns:
            str: Path to the generated diagram
        """
        try:
            import graphviz
            dot = graphviz.Digraph(comment='System Architecture')
            dot.attr(rankdir='TB')

            # Define node styles
            dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')

            # Add components
            components = {
                'web': 'Web Interface\n(Streamlit)',
                'auth': 'Authentication\n(Flask-Login)',
                'inventory': 'Inventory Manager',
                'db': 'PostgreSQL\nDatabase',
                'api': 'Unimall B2B\nAPI Client'
            }

            for key, label in components.items():
                dot.node(key, label)

            # Add relationships with custom styling
            relationships = [
                ('web', 'auth', 'authenticates'),
                ('auth', 'inventory', 'manages'),
                ('inventory', 'db', 'stores/retrieves'),
                ('inventory', 'api', 'syncs')
            ]

            for src, dst, label in relationships:
                dot.edge(src, dst, label)

            # Save diagram
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            filename = f"system_architecture_{timestamp}"
            output_path = os.path.join(self.output_dir, filename)
            dot.render(output_path, format='svg', cleanup=True)
            logger.info(f"Generated system architecture diagram: {output_path}.svg")
            return f"{output_path}.svg"

        except Exception as e:
            logger.error(f"Error generating system diagram: {str(e)}")
            raise

    def capture_ui_screenshot(self, url: str, element_id: Optional[str] = None) -> str:
        """
        Capture screenshot of the web interface.

        Args:
            url (str): URL to capture
            element_id (Optional[str]): Specific element ID to capture

        Returns:
            str: Path to the screenshot
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            with self.get_chrome_driver() as driver:
                logger.info(f"Navigating to {url}")
                driver.get(url)

                # Add a small delay to ensure page loads
                driver.implicitly_wait(5)

                if element_id:
                    logger.info(f"Waiting for element: {element_id}")
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, element_id))
                    )
                    screenshot = element.screenshot_as_png
                else:
                    logger.info("Capturing full page screenshot")
                    screenshot = driver.get_screenshot_as_png()

                timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                filename = f"ui_screenshot_{timestamp}.png"
                output_path = os.path.join(self.output_dir, filename)

                with open(output_path, 'wb') as f:
                    f.write(screenshot)

                logger.info(f"Saved screenshot to: {output_path}")
                return output_path

        except Exception as e:
            logger.error(f"Error capturing screenshot: {str(e)}")
            raise

    def generate_documentation_assets(self, base_url: str = "http://0.0.0.0:8501") -> Dict[str, List[str]]:
        """
        Generate all documentation assets.

        Args:
            base_url (str): Base URL of the application

        Returns:
            Dict[str, List[str]]: Dictionary mapping asset types to file paths
        """
        generated_assets = {
            'diagrams': [],
            'screenshots': []
        }

        try:
            # Generate system architecture diagram
            diagram_path = self.generate_system_architecture_diagram()
            generated_assets['diagrams'].append(diagram_path)
            logger.info("Generated system architecture diagram")

            # Wait a bit for the Streamlit app to be ready
            import time
            time.sleep(5)

            # Capture UI screenshots
            sections = {
                'main': None,  # Full page screenshot
                'login-form': 'login-form',
                'inventory-section': 'inventory-section',
                'export-section': 'export-section'
            }

            for section_name, section_id in sections.items():
                try:
                    screenshot_path = self.capture_ui_screenshot(base_url, section_id)
                    generated_assets['screenshots'].append(screenshot_path)
                    logger.info(f"Generated screenshot for section: {section_name}")
                except Exception as e:
                    logger.error(f"Error capturing {section_name}: {str(e)}")

            # Save asset manifest
            manifest_path = os.path.join(self.output_dir, 'asset_manifest.json')
            with open(manifest_path, 'w') as f:
                json.dump(generated_assets, f, indent=2)
            logger.info(f"Generated asset manifest: {manifest_path}")

            return generated_assets

        except Exception as e:
            logger.error(f"Error generating documentation assets: {str(e)}")
            raise