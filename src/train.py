#!/usr/bin/env python3
"""
Basic ML training script demonstrating MLOps workflow.
"""

import os
import sys
import json
import pickle
import logging
from datetime import datetime
from typing import Tuple, Dict, Any

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_synthetic_data(n_samples: int = 1000, n_features: int = 20) -> Tuple[np.ndarray, np.ndarray]:
    """Create synthetic dataset for demonstration purposes."""
    logger.info(f"Creating synthetic dataset with {n_samples} samples and {n_features} features")
    
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=15,
        n_redundant=5,
        random_state=42
    )
    return X, y


def preprocess_data(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, StandardScaler]:
    """Split and preprocess the data."""
    logger.info("Splitting data into train/test sets")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info("Scaling features")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model."""
    logger.info("Training Random Forest model")
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    logger.info("Model training completed")
    
    return model


def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
    """Evaluate the trained model."""
    logger.info("Evaluating model performance")
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    logger.info(f"Test accuracy: {accuracy:.4f}")
    
    metrics = {
        "accuracy": accuracy,
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
        "timestamp": datetime.now().isoformat()
    }
    
    return metrics


def save_model_and_artifacts(model: RandomForestClassifier, scaler: StandardScaler, 
                           metrics: Dict[str, Any], model_name: str = "random_forest_model") -> str:
    """Save trained model and associated artifacts."""
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    os.makedirs(models_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(models_dir, f"{model_name}_{timestamp}.pkl")
    scaler_path = os.path.join(models_dir, f"{model_name}_scaler_{timestamp}.pkl")
    metrics_path = os.path.join(models_dir, f"{model_name}_metrics_{timestamp}.json")
    
    logger.info(f"Saving model to {model_path}")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    logger.info(f"Saving scaler to {scaler_path}")
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    
    logger.info(f"Saving metrics to {metrics_path}")
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    return model_path


def main():
    """Main training pipeline."""
    logger.info("Starting ML training pipeline")
    
    try:
        # Create synthetic data
        X, y = create_synthetic_data(n_samples=1000, n_features=20)
        
        # Preprocess data
        X_train, X_test, y_train, y_test, scaler = preprocess_data(X, y)
        
        # Train model
        model = train_model(X_train, y_train)
        
        # Evaluate model
        metrics = evaluate_model(model, X_test, y_test)
        
        # Save model and artifacts
        model_path = save_model_and_artifacts(model, scaler, metrics)
        
        logger.info(f"Training pipeline completed successfully!")
        logger.info(f"Model saved to: {model_path}")
        logger.info(f"Final accuracy: {metrics['accuracy']:.4f}")
        
    except Exception as e:
        logger.error(f"Training pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()