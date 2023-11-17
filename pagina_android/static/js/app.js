document.addEventListener('DOMContentLoaded', function() {
	let index = 0;
	const cards = document.querySelectorAll('.card');
  
	function mostrarSiguienteCard() {
	  cards[index].classList.remove('active');
	  cards[index].style.opacity = 0;
	  
	  index = (index + 1) % cards.length;
	  
	  cards[index].classList.add('active');
	  cards[index].style.opacity = 1;
	}
  
	setInterval(mostrarSiguienteCard, 3000); // Cambiar de tarjeta cada 3 segundos
  });
  