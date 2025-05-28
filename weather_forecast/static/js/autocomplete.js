document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("city-input");

    if (!input) return;

    input.addEventListener("input", function () {
        const query = this.value;
        if (query.length < 2) return;

        fetch(`/city-autocomplete/?q=${query}`)
            .then(res => res.json())
            .then(data => {
                // Можно расширить до полноценного списка подсказок
                console.log("Suggestions:", data);
            });
    });
});