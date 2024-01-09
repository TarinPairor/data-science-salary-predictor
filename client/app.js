function getWorkYearValue() {
  var uiBathrooms = document.getElementsByName("uiwork-year");
  for (var i in uiBathrooms) {
    if (uiBathrooms[i].checked) {
      return parseInt(i) + 1;
    }
  }
  return -1; // Invalid Value
}

function onClickedEstimatePrice() {
  console.log("Estimate salary button clicked");
  var work_year = getWorkYearValue();
  var job_category = document.getElementById("ui_job_category");
  var employee_residence = document.getElementById("ui_employee_residence");
  var experience_level = document.getElementById("ui_experience_level");
  var work_setting = document.getElementById("ui_work_setting");
  var company_location = document.getElementById("ui_company_location");
  var company_size = document.getElementById("ui_company_size");

  var estSalary = document.getElementById("uiEstimatedSalary");
  var url = "http://127.0.0.1:5000/predict";
  console.log("Up to here");
  console.log(parseInt(work_year));
  console.log(parseInt(job_category));
  $.ajax({
    url: url,
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      work_year: parseInt(work_year),
      job_category: job_category.value,
      employee_residence: employee_residence.value,
      experience_level: experience_level.value,
      work_setting: work_setting.value,
      company_location: company_location.value,
      company_size: company_size.value,
    }),
    dataType: "json",
    success: function (data, status) {
      console.log("Data:", data);

      if (data && data.estimated_salary !== undefined) {
        estSalary.innerHTML =
          "<h2>" + data.estimated_salary.toString() + "<h2>";
      } else {
        estSalary.innerHTML = "<h2>No estimated salary available<h2>";
      }

      console.log(status);
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
}

function onPageLoad() {
  console.log("document loaded");

  // Define the categories
  var categories = [
    "job_category",
    "employee_residence",
    "experience_level",
    "work_setting",
    "company_location",
    "company_size",
  ];

  categories.forEach(function (category) {
    fetchDataForCategory(category);
  });
}

function fetchDataForCategory(category) {
  var url = "http://127.0.0.1:5000/get_vars/" + category;

  $.get(url, function (data, status) {
    console.log("got response for get_" + category + " request");
    console.log(data);
    if (data) {
      var options = data;
      var uiDropdown = document.getElementById("ui_" + category);
      if (uiDropdown) {
        $("#" + uiDropdown.id).empty();
        for (var i in options) {
          var opt = new Option(options[i], options[i]); // Add both value and text
          $("#" + uiDropdown.id).append(opt);
          console.log("Option: " + opt);
        }
      } else {
        console.error("Element not found: " + "ui_" + category);
      }
    }
  });
}

window.onload = onPageLoad;
