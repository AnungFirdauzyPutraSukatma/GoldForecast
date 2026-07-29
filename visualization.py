import matplotlib.pyplot as plt
import numpy as np

labels = [
    'Time Bars',
    'Tick Volume Bars'
]

cv_values = [
    43.49,
    34.83
]

plt.figure(figsize=(6,4))

plt.bar(
    labels,
    cv_values
)

plt.ylabel('Coefficient of Variation')
plt.title('Perbandingan Nilai CV')

for i, v in enumerate(cv_values):
    plt.text(
        i,
        v + 0.5,
        str(v),
        ha='center'
    )

plt.tight_layout()

plt.savefig(
    'cv_comparison.png',
    dpi=300
)

plt.show()


cm = np.array([
    [12, 0, 27],
    [10, 1, 25],
    [15, 3, 31]
])

plt.figure(figsize=(6,5))

plt.imshow(cm)

plt.colorbar()

labels = ['-1', '0', '1']

plt.xticks(
    range(3),
    labels
)

plt.yticks(
    range(3),
    labels
)

plt.xlabel('Prediksi')
plt.ylabel('Aktual')
plt.title('Confusion Matrix')

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):

        plt.text(
            j,
            i,
            cm[i, j],
            ha='center',
            va='center'
        )

plt.tight_layout()

plt.savefig(
    'confusion_matrix.png',
    dpi=300
)

plt.show()

labels = ['-1', '0', '1']
values = [196, 180, 241]

plt.figure(figsize=(6,4))

plt.bar(
    labels,
    values
)

plt.xlabel('Label')
plt.ylabel('Jumlah Data')
plt.title('Distribusi Label')

for i, v in enumerate(values):
    plt.text(
        i,
        v + 2,
        str(v),
        ha='center'
    )

plt.tight_layout()

plt.savefig(
    'label_distribution.png',
    dpi=300
)

plt.show()