document.addEventListener('DOMContentLoaded', function () {
	const steps = document.querySelectorAll('.step');
	const progressItems = document.querySelectorAll('#progressbar li');
	const nextBtns = document.querySelectorAll('.next-btn');
	const backBtns = document.querySelectorAll('.back-btn');
	const form = document.getElementById('student_information_form');

	let currentStep = 0;

	function showStep(index) {
		steps.forEach((step, i) => {
			if (i === index) {
				step.classList.add('active');
				step.style.display = 'block';
			} else {
				step.classList.remove('active');
				step.style.display = 'none';
			}
			progressItems[i].classList.toggle('active', i <= index);
		});
	
		const progressWidth = ((index) / (steps.length - 1)) * 100;
		const progressLine = document.getElementById('progress-line');
		if (progressLine) {
			progressLine.style.width = progressWidth + '%';
		}
	}
	
	
	

	function validateStep(index) {
		const inputs = steps[index].querySelectorAll('input, select, textarea');
		let isValid = true;

		inputs.forEach((input) => {
			if (input.hasAttribute('required') && !input.value.trim()) {
				input.classList.add('is-invalid');
				isValid = false;
			} else {
				input.classList.remove('is-invalid');
			}

			// Real-time validation: remove is-invalid when filled
			input.addEventListener('input', () => {
				if (input.value.trim()) {
					input.classList.remove('is-invalid');
				}
			});
		});

		return isValid;
	}

	nextBtns.forEach((btn) => {
		btn.addEventListener('click', () => {
			if (validateStep(currentStep)) {
				if (currentStep < steps.length - 1) {
					currentStep++;
					showStep(currentStep);
				}
			}
		});
	});

	backBtns.forEach((btn) => {
		btn.addEventListener('click', () => {
			if (currentStep > 0) {
				currentStep--;
				showStep(currentStep);
			}
		});
	});

	showStep(currentStep);
});
