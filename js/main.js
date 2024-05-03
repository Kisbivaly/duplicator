(function () {
  const win = window
  const doc = document.documentElement

  doc.classList.remove('no-js')
  doc.classList.add('js')

  // Reveal animations
  if (document.body.classList.contains('has-animations')) {
    /* global ScrollReveal */
    const sr = window.sr = ScrollReveal()

    sr.reveal('.hero-title, .hero-paragraph, .hero-form', {
      duration: 1000,
      distance: '40px',
      easing: 'cubic-bezier(0.5, -0.01, 0, 1.005)',
      origin: 'bottom',
      interval: 150
    })
  }

  // Moving objects
  const movingObjects = document.querySelectorAll('.is-moving-object')

  // Throttling
  function throttle (func, milliseconds) {
    let lastEventTimestamp = null
    let limit = milliseconds

    return (...args) => {
      let now = Date.now()

      if (!lastEventTimestamp || now - lastEventTimestamp >= limit) {
        lastEventTimestamp = now
        func.apply(this, args)
      }
    }
  }

  // Init vars
  let mouseX = 0
  let mouseY = 0
  let scrollY = 0
  let coordinateX = 0
  let coordinateY = 0
  let winW = doc.clientWidth
  let winH = doc.clientHeight

  // Move Objects
  function moveObjects (e, object) {
    mouseX = e.pageX
    mouseY = e.pageY
    scrollY = win.scrollY
    coordinateX = (winW / 2) - mouseX
    coordinateY = (winH / 2) - (mouseY - scrollY)

    for (let i = 0; i < object.length; i++) {
      const translatingFactor = object[i].getAttribute('data-translating-factor') || 20
      const rotatingFactor = object[i].getAttribute('data-rotating-factor') || 20
      const perspective = object[i].getAttribute('data-perspective') || 500
      let tranformProperty = []

      if (object[i].classList.contains('is-translating')) {
        tranformProperty.push('translate(' + coordinateX / translatingFactor + 'px, ' + coordinateY / translatingFactor + 'px)')
      }

      if (object[i].classList.contains('is-rotating')) {
        tranformProperty.push('perspective(' + perspective + 'px) rotateY(' + -coordinateX / rotatingFactor + 'deg) rotateX(' + coordinateY / rotatingFactor + 'deg)')
      }

      if (object[i].classList.contains('is-translating') || object[i].classList.contains('is-rotating')) {
        tranformProperty = tranformProperty.join(' ')

        object[i].style.transform = tranformProperty
        object[i].style.transition = 'transform 1s ease-out'
        object[i].style.transformStyle = 'preserve-3d'
        object[i].style.backfaceVisibility = 'hidden'
      }
    }
  }

  // Call function with throttling
  if (movingObjects) {
    win.addEventListener('mousemove', throttle(
      function (e) {
        moveObjects(e, movingObjects)
      },
      150
    ))
  }
}())

function openPreview() {
const url = document.getElementById('url').value.trim();
if (url) {
  window.open(`/preview?url=${encodeURIComponent(url)}`);
} else {
  showError('Please enter a valid URL.');
}
}

async function initiatePaymentAndDownload() {
  const url = document.getElementById('url').value.trim();
  const amount = 500000; 

  if (url) {
    try {
      
      const paymentResponse = await fetch(`/initiate-payment?url=${encodeURIComponent(url)}&amount=${amount}`);
      const paymentData = await paymentResponse.json();

      if (paymentResponse.ok) {
        
        window.location.href = paymentData.paymentLink;
      } else {
        
        showError(`An error occurred while initiating payment: ${paymentData.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('An error occurred:', error);
      showError('An error occurred while initiating payment.');
    }
  } else {
    showError('Please enter a valid URL.');
  }
}

document.getElementById('saveToDevice').addEventListener('click', initiatePaymentAndDownload);



const form = document.getElementById('download-form');
const progressContainer = document.getElementById('progress-container');
const progressBar = document.getElementById('progress-bar');
const progressStatus = document.getElementById('progress-status');

// Define the "Save to Device" button element
const saveToDeviceButton = document.getElementById('saveToDevice');

async function downloadWebsite() {
  // Reset the "Save to Device" button to be hidden
  saveToDeviceButton.style.display = 'none';

  const url = document.getElementById('url').value.trim();

  if (url) {
    form.style.display = 'none';
    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';
    progressStatus.innerText = 'Initializing...';

    try {
      const response = await fetch(`/download?url=${encodeURIComponent(url)}`);
      const data = await response.json();

      if (response.ok) {
        // Update the "Save to Device" button attributes
        saveToDeviceButton.style.display = 'block';
        saveToDeviceButton.href = `${data.downloadUrl}`;
        saveToDeviceButton.download = `${data.zipFileName}`;
      } else {
        // Handle error
        showError(`An error occurred: ${data.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('An error occurred:', error);
      showError('An error occurred while processing the download.');
    } finally {
      // Optional: You can add cleanup code here if needed
      progressContainer.style.display = 'none';
      form.style.display = 'block';
    }
  } else {
    showError('Please enter a valid URL.');
  }
}





function extractHostname(url) {
  let hostname;
  if (url.indexOf('://') > -1) {
    hostname = url.split('/')[2];
  } else {
    hostname = url.split('/')[0];
  }
  hostname = hostname.split(':')[0];
  hostname = hostname.split('?')[0];
  return hostname;
}
function showError(message) {
  const errorContainer = document.getElementById('error-container');
  const errorMessage = document.getElementById('error-message');
  errorMessage.textContent = message;
  errorContainer.style.display = 'block';
  form.style.display = 'block';
  progressContainer.style.display = 'none';
}

function showPopup() {
  document.getElementById("popup").style.display = "block";
}

function hidePopup() {
  document.getElementById("popup").style.display = "none";
}
