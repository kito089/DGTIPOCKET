document.addEventListener("DOMContentLoaded", function () {
	const carousel = document.querySelector(".carousel");
	const cards = document.querySelectorAll(".card");

	let currentIndex = 0;

	function showCard(index) {
		const newPosition = -index * 100 + "%";
		carousel.style.transform = "translateX(" + newPosition + ")";
	}

	function nextCard() {
		currentIndex = (currentIndex + 1) % cards.length;
		showCard(currentIndex);
	}

	setInterval(nextCard, 3000); // Cambia la tarjeta cada 3 segundos (ajusta según sea necesario)
});