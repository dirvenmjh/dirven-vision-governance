#!/usr/bin/env python3
"""
Run all phases: fetch data → train models → predictions → CSV submission
Complete end-to-end pipeline
"""

import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Create logs directory
Path('logs').mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/full_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_phase(phase_num: int, script_name: str, description: str) -> bool:
    """Run a single phase"""
    
    logger.info("\n" + "="*70)
    logger.info(f"PHASE {phase_num}: {description}")
    logger.info("="*70)
    
    try:
        result = subprocess.run([sys.executable, script_name], check=True)
        logger.info(f"✓ Phase {phase_num} complete")
        return True
    
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ Phase {phase_num} failed: {e}")
        return False
    
    except Exception as e:
        logger.error(f"✗ Phase {phase_num} error: {e}")
        return False


def main():
    logger.info("="*70)
    logger.info("NUMERAI CRYPTO - FULL PIPELINE")
    logger.info("Individual Models for 504 Symbols")
    logger.info("="*70)
    logger.info(f"Start time: {datetime.now()}")
    
    phases = [
        (1, "1_fetch_data.py", "Fetch Price Data for 504 Symbols"),
        (2, "2_train_models.py", "Train V6 Models for 504 Symbols"),
        (3, "3_generate_predictions.py", "Generate Predictions"),
        (4, "4_create_submission.py", "Create Submission CSV"),
    ]
    
    results = []
    
    for phase_num, script, description in phases:
        success = run_phase(phase_num, script, description)
        results.append((phase_num, description, success))
        
        if not success:
            logger.error(f"Pipeline stopped at phase {phase_num}")
            break
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("PIPELINE SUMMARY")
    logger.info("="*70)
    
    for phase_num, description, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        logger.info(f"Phase {phase_num}: {status} - {description}")
    
    all_success = all(r[2] for r in results)
    
    if all_success:
        logger.info("\n" + "="*70)
        logger.info("✓ PIPELINE COMPLETE - READY TO UPLOAD")
        logger.info("="*70)
        logger.info(f"File: numerai_submission_final.csv")
        logger.info(f"Upload to: https://numerai.com/tournaments/crypto")
        logger.info(f"Model ID: e64d764d-301c-4ea8-9107-1fe7d5d6c39f")
        logger.info(f"End time: {datetime.now()}")
        return 0
    else:
        logger.error("\n✗ PIPELINE FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
