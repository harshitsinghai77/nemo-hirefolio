// Company Name: The name of the company where the job is located.
// Job Title: The specific job title you applied for.
// Job Posting Link: Link directly to the job posting you applied to.
// Application Status: Pending

// Applied: Yes/No did you apply?
// Application Date: Date you submitted your application.

// Application Method: How did you apply (e.g., online portal, email, recruiter)?
// Yes/No did you follow up after applying?

// Contact Person: Name and contact information of anyone you know at the company (referral contact).
// Cold Email Sent: Yes/No did you send a cold email to someone at the company?
// Notes: Any additional notes or details about the job or application process.
// Next Steps: Actionable steps you'll take next (e.g., follow up, research company).

async function getSampleData() {
  const response = await fetch("/get-job");
  const responseFromAPI = await response.json();

  const columns = responseFromAPI["columns"];
  const dataFromAPI = responseFromAPI["data"];

  return {
    columns,
    dataFromAPI,
  };
}

function formatDate(date) {
  const day = String(date.getDate()).padStart(2, "0");
  const month = date.toLocaleString("default", { month: "short" });
  const year = date.getFullYear();
  return `${day} ${month} ${year}`;
}

function getEditor(colIndex, rowIndex, value, parent, column, row, data) {
  // colIndex, rowIndex of the cell being edited
  // value: value of cell before edit
  // parent: edit container (use this to append your own custom control)
  // column: the column object of editing cell
  // row: the row of editing cell
  // data: array of all rows

  const $input = document.createElement("input");
  if (column.id == "application_date") {
    $input.type = "date";
  }

  parent.appendChild($input);
  return {
    // called when cell is being edited
    initValue(value) {
      $input.focus();
      $input.value = value;
    },
    // called when cell value is set
    setValue(value) {
      $input.value = value;
      const updatedRow = [...row]; // Create a copy of the row object
      updatedRow[column.colIndex] = {
        ...updatedRow[column.colIndex],
        content: value,
      };

      let newRow = false;
      // Check if the deta key is empty i.e new row is added.
      if (!row[row.length - 1].content) {
        newRow = true;
        datatable.freeze();
      }

      makePostRequest("/update-job", updatedRow)
        .then(async (responseData) => {
          // newRow True means that a new is added, add the key to the new row and update the row.
          if (responseData.new_key && newRow) {
            row[row.length - 1].content = responseData.new_key;
            datatable.refreshRow(row, row.meta.rowIndex);
            datatable.unfreeze();
          }
        })
        .catch((error) => {
          // Handle errors here
          console.log("error", error);
        });
    },
    // value to show in cell
    getValue() {
      // if (column.id == "follow_up") {
      //   const date = new Date($input.value);
      //   return formatDate(date); // Use a formatting function
      // }
      return $input.value;
    },
  };
}

async function makePostRequest(url, data) {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const responseData = await response.json(); // Assuming JSON response
    return responseData;
  } catch (error) {
    console.error("Error:", error);
  }
}

async function deleteJob(url) {
  try {
    const response = await fetch(url, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`DELETE request failed with status ${response.status}`);
    }

    await response.json(); // Assuming JSON response
  } catch (error) {
    console.error("Error deleting job:", error);
  }
}

async function refreshTable() {
  const { columns, dataFromAPI } = await getSampleData();
  datatable.refresh(dataFromAPI, columns);
}

// Get references to the button and DataTable container
const addRowButton = document.getElementById("add-new-row");
const removeRowButton = document.getElementById("remove-selected-row");

// Add event listener to the button
addRowButton.addEventListener("click", () => {
  datatable.appendRows([[]]); // Append an empty row
});

removeRowButton.addEventListener("click", async () => {
  const selectedRowIndex = datatable.rowmanager.getCheckedRows();

  const allRows = datatable.getRows();
  const rowsToDelete = selectedRowIndex.map((rowIndex) => allRows[rowIndex]);
  const rowDeleteKeys = rowsToDelete.map(
    (elem) => elem.find((c) => c.column.id === "key").content
  );

  // Send rowsToDelete to the DELETE API
  datatable.freeze();
  rowDeleteKeys.forEach(
    async (rowId) => await deleteJob(`/delete-job/${rowId}`)
  );

  // Untick selectedRows
  selectedRowIndex.forEach((rowIndex) =>
    datatable.rowmanager.checkRow(rowIndex, 0)
  );
  await refreshTable();
  datatable.unfreeze();
});
