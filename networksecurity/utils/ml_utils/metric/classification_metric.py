from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact

from sklearn.metrics import precision_score, recall_score, f1_score

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)

        classification_metric_artifact = ClassificationMetricArtifact(
            f1_score=f1,
            precision_score = precision,
            recall_score = recall
        )

        return classification_metric_artifact

    except Exception as e:
        raise NetworkSecurityException(e, sys)