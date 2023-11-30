function updateDateTime() {
    let dateTimeElement = document.getElementById('datetime');
    let now = new Date();
    
    // Format the date and time
    let formattedDateTime = now.getFullYear() + '-' +
                            ('0' + (now.getMonth() + 1)).slice(-2) + '-' +
                            ('0' + now.getDate()).slice(-2) + ' ' +
                            ('0' + now.getHours()).slice(-2) + ':' +
                            ('0' + now.getMinutes()).slice(-2) + ':' +
                            ('0' + now.getSeconds()).slice(-2);

    // Update the content of the element
    dateTimeElement.textContent = formattedDateTime;
  }

  // Update the date and time initially
  updateDateTime();

  // Update the date and time every second
  setInterval(updateDateTime, 1000);

// Function to adjust views
  function fetchTasksByView(view) {
    fetch(`/tasks/${view}`)
        .then(response => response.json())
        .then(data => {
            // Clear existing tasks
            const taskContainer = document.getElementById('taskContainer');
            taskContainer.innerHTML = '';

            // Render tasks for the selected view
            data.tasks.forEach(task => renderTask(task, taskContainer));
        })
        .catch(error => console.error('Error fetching tasks:', error));
}


// Add an event listener to the checkboxes
document.addEventListener('DOMContentLoaded', function() {
  let checkboxes = document.querySelectorAll('.checkbox');

  checkboxes.forEach(function(checkbox) {
      checkbox.addEventListener('change', function() {
          let taskSecret = this.getAttribute('data-task-secret');
          updateTaskCompletion(taskSecret, this.checked);
          location.reload(true);
      });
  });
});

// Function to send a POST request to update task completion
function updateTaskCompletion(taskSecret, completed) {
  fetch(`/tasks/complete/${taskSecret}`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          completed: completed,
      }),
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then(data => {
      // Handle the response if needed
      console.log(data);
      
  })
  .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
  });
}
const currentPath = window.location.pathname;

// Function to highlight the active link
function highlightActiveLink() {
    const links = document.querySelectorAll('.navigation a');
    links.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Call the function to highlight the active link
highlightActiveLink();
