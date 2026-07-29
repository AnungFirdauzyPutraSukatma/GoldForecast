import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import CategoricalNB

from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


class NaiveBayesModel:

    def __init__(
        self,
        dataset,
        test_size=0.2,
        random_state=42
    ):

        if isinstance(dataset, str):

            self.data = pd.read_csv(
                dataset
            )

        elif isinstance(
            dataset,
            pd.DataFrame
        ):

            self.data = dataset.copy()

        else:

            raise TypeError(
                "dataset harus berupa DataFrame atau path csv"
            )

        self.test_size = test_size

        self.random_state = random_state

    def process(self):

        # ==========================
        # Feature & Target
        # ==========================

        X = self.data[

            [
                'RSI',
                'STOCH_D',
                'MACD_HIST'
            ]

        ]

        y = self.data['LABEL']

        # ==========================
        # Train Test Split
        # ==========================

        X_train, X_test, y_train, y_test = (

            train_test_split(

                X,
                y,

                test_size=self.test_size,

                random_state=self.random_state,

                stratify=y

            )

        )

        # ==========================
        # Model
        # ==========================

        model = CategoricalNB()

        model.fit(
            X_train,
            y_train
        )

        y_pred = model.predict(
            X_test
        )

        # ==========================
        # Evaluation
        # ==========================

        accuracy = accuracy_score(
            y_test,
            y_pred
        )

        precision = precision_score(
            y_test,
            y_pred,
            average='weighted',
            zero_division=0
        )

        recall = recall_score(
            y_test,
            y_pred,
            average='weighted',
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            y_pred,
            average='weighted',
            zero_division=0
        )

        cm = confusion_matrix(
            y_test,
            y_pred
        )

        print("\n===== HASIL EVALUASI =====")

        print(
            f"Accuracy  : {accuracy:.4f}"
        )

        print(
            f"Precision : {precision:.4f}"
        )

        print(
            f"Recall    : {recall:.4f}"
        )

        print(
            f"F1 Score  : {f1:.4f}"
        )

        print(
            "\nConfusion Matrix:"
        )

        print(cm)

        print(
            "\nClassification Report:"
        )

        print(

            classification_report(
                y_test,
                y_pred,
                zero_division=0
            )

        )

        report = classification_report(
            y_test,
            y_pred,
            output_dict=True
        )
        report_df = pd.DataFrame(
            report
        ).transpose()

        report_df.to_csv(
            'classification_report.csv'
        )

        # print(pd.Series(y_pred).value_counts())

        return {

            'model': model,

            'accuracy': accuracy,

            'precision': precision,

            'recall': recall,

            'f1': f1,

            'confusion_matrix': cm

        }