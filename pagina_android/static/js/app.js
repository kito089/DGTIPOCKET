document.addEventListener('DOMContentLoaded', function() {
	let index = 0;
	const cards = document.querySelectorAll('.card');
  
	function mostrarSiguienteCard() {
	  cards[index].classList.remove('active');
	  index = (index + 1) % cards.length;
	  cards[index].classList.add('active');
	}
  
	setInterval(mostrarSiguienteCard, 3000); // Cambiar de tarjeta cada 3 segundos
  });
  