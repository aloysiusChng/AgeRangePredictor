const age_ranges_index = {
    0: "0-20",
    1: "21-40",
    2: "41-60",
    3: "61-80"
}

document.addEventListener('DOMContentLoaded', async function() {
    const loadingContainer = document.getElementById('loading-container');
    const imageUploadButton = document.getElementById('image-upload-btn');
    const predictButton = document.getElementById('predict-btn');
    const imageUploadContainer = document.getElementById('image-upload-container');
    const imagePreview = document.getElementById('image-preview');
    const predictionResultsContainer = document.getElementById('prediction-results-container');
    const predictedAgeLabel = document.getElementById('predicted-age-label');
    const returnButton = document.getElementById('return-btn');

    imageUploadButton.addEventListener('change', async function() {
        if (imageUploadButton.files.length === 0) {
            predictButton.disabled = true;
            return;
        }
        predictButton.disabled = false;
    });

    predictButton.addEventListener('click', async function() {
        if ( predictButton.disabled ) { return; }
        loadingContainer.style.display = 'block';
        predictButton.disabled = true;
        const file = imageUploadButton.files[0];

        const upload_body = new FormData();
        upload_body.append('file', file);
        const upload_request = await fetch(
            '/api/upload_file',
            {
                method: 'POST',
                body: upload_body
            }
        )
        if (!upload_request.ok) {
            console.error('Failed to upload file');
            return;
        }
        const upload_response = await upload_request.json();
        const file_hash = upload_response.file_hash;

        const prediction_request = await fetch(
            `/api/predict_age/${file_hash}`
        );
        if (!prediction_request.ok) {
            console.error('Failed to predict age');
            return;
        }
        const prediction_response = await prediction_request.json();
        const age_index = prediction_response.predicted_class;
        const age_range = age_ranges_index[age_index];
        imageUploadContainer.style.display = 'none';
        imagePreview.src = URL.createObjectURL(file);
        imagePreview.style.display = 'block';
        loadingContainer.style.display = 'none';
        predictedAgeLabel.textContent = `Predicted Age: ${age_range}`;
        predictionResultsContainer.style.display = 'block';
        predictButton.disabled = false;
    });

    returnButton.addEventListener('click', function() {
        imageUploadContainer.style.display = 'block';
        predictButton.disabled = true;
        imagePreview.style.display = 'none';
        predictionResultsContainer.style.display = 'none';
        imageUploadButton.value = '';
    });
});