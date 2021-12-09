(function () {
	"use strict";

	let forms = document.querySelectorAll('.email-form');

	forms.forEach(function (e) {
		e.addEventListener('submit', function (event) {
			event.preventDefault();

			let thisForm = this;

			let action = thisForm.getAttribute('action');
			let recaptcha = thisForm.getAttribute('data-recaptcha-site-key');

			if (!action) {
				displayError(thisForm, 'The form action property is not set!')
				return;
			}
			thisForm.querySelector('.loading').classList.add('d-block');
			thisForm.querySelector('.error-message').classList.remove('d-block');
			thisForm.querySelector('.sent-message').classList.remove('d-block');

			let formData = new FormData(thisForm);
			if(document.querySelector('input[type="file"]')) formData.append('file', document.querySelector('input[type="file"]').files[0])

			if (recaptcha) {
				if (typeof grecaptcha !== "undefined") {
					grecaptcha.ready(function () {
						try {
							grecaptcha.execute(recaptcha, { action: 'form_submit' })
								.then(token => {
									formData.set('recaptcha-response', token);
									form_submit(thisForm, action, formData);
								})
						} catch (error) {
							displayError(thisForm, error)
						}
					});
				} else {
					displayError(thisForm, 'The reCaptcha javascript API url is not loaded!')
				}
			} else {
				form_submit(thisForm, action, formData);
			}
		});
	});

	function displayError(thisForm, error) {
		thisForm.querySelector('.loading').classList.remove('d-block');
		thisForm.querySelector('.error-message').innerHTML = error;
		thisForm.querySelector('.error-message').classList.add('d-block');
		setTimeout(() => {
			thisForm.querySelector('.error-message').classList.remove('d-block');
			thisForm.querySelector('.error-message').innerHTML = '';
		},3000)
	}

	async function form_submit(thisForm, action, formData) {
		try {
			const response = await fetch(action, {
				method: 'POST',
				body: formData,
				headers: { 'X-Requested-With': 'XMLHttpRequest' }
			})

			const data = await response.text()
			if (response.ok && !response.redirected) {
				thisForm.querySelector('.loading').classList.remove('d-block');
				if (data.trim() == 'OK') {
					thisForm.querySelector('.sent-message').classList.add('d-block');
					setTimeout(() => thisForm.querySelector('.sent-message').classList.remove('d-block'),1000)
					thisForm.reset();
				} else {
					throw new Error(data ? data : 'Form submission failed and no error message returned from: ' + action);
				}
			}
			else if (response.redirected) {
				thisForm.querySelector('.loading').classList.remove('d-block');
				thisForm.querySelector('.sent-message').classList.add('d-block');
				setTimeout(() => {
					thisForm.querySelector('.sent-message').classList.remove('d-block')
					window.location.href = response.url
				},3000)
			}
			else throw new Error(`${data}`)

		} catch (error) {
			displayError(thisForm, error)
		}
	}

})();