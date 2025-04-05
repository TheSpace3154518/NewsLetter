// Create a new FormData object
function unsubscribe(id) {
    const formData = new FormData();

    // Add fields with custom names
    formData.append('entry.2074575139', id);

    // Send POST request using fetch
    fetch('https://docs.google.com/forms/d/e/1FAIpQLSfLrJUkEicSEMg8UU_mlOjNA72AFaqKppUwhUvYAC4tplE5tA/formResponse', {
        method: 'POST',
        body: formData
    })
    .catch(error => {
        console.error('Error:', error);
    });
}