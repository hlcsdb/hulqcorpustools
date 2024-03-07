"use strict";

const advancedColumns = document.querySelectorAll('.advanced');
const showMore = document.querySelector('#show-columns');
var columnsShowing = false;
showMore.addEventListener('click', (e) => {
  if (columnsShowing == false) {
    showMore.textContent = 'hide';
    columnsShowing = true;
    for (const cell of advancedColumns) {
      cell.style.display = 'table-cell';
    }
  } else {
    showMore.textContent ='show more';
    columnsShowing = false
    for (const cell of advancedColumns) {
      cell.style.display = 'none';
    }
    showMore.textContent = 'show more';
  }

})

function sortTable(table) {
  const tBody = table.tBodies[0];
  const rows= Array.from(tBody.rows);
  const headerCells = table.tHead.rows[0].cells;
  for (const th of headerCells) {
    const sortArrow = th.querySelector('.sort-arrow')
    let otherSortArrows = table.querySelectorAll(".sort-arrow")
    otherSortArrows = Array.from(otherSortArrows).filter(arrow => arrow !== sortArrow);
    let otherHeaders = Array.from(headerCells).filter(header => header !== th);

    const cellIndex = th.cellIndex;

    th.addEventListener("click", () => {

      if (th.classList.contains("descending"))
      {
        rows.sort((tr1, tr2) => {
          const tr1Text = tr1.cells[cellIndex].textContent;
          const tr2Text = tr2.cells[cellIndex].textContent;
          return tr1Text.localeCompare(tr2Text);
          });
        th.classList.remove("descending");
        th.classList.add("ascending");
        sortArrow.textContent="⏶";

      } else {
        rows.sort((tr1, tr2) => {
          const tr2Text = tr1.cells[cellIndex].textContent;
          const tr1Text = tr2.cells[cellIndex].textContent;
          return tr1Text.localeCompare(tr2Text);
        });
        th.classList.remove("ascending");
        th.classList.add("descending");
        sortArrow.textContent="⏷";
      }
      // change all other arrows to blank
      otherSortArrows.forEach(function(sortArrow) {
        sortArrow.classList.add("invisible")
      })
      sortArrow.classList.remove("invisible")

      otherHeaders.forEach(header => {
        header.classList.remove("ascending");
        header.classList.remove("descending");
      });
      tBody.append(...rows);
    });
  }
}

// const definedWordsResults = document.querySelector("#defined-results");
// const definedWordsSort = sortTable(definedWordsResults);

const recognizedWordsResults = document.querySelector("#recognized-results");
const recognizedWordsSort = sortTable(recognizedWordsResults);

const unrecognizedWordsResults = document.querySelector("#unrecognized-results");
const unrecognizedWordsSort = sortTable(unrecognizedWordsResults);

const infoBoxes = document.querySelectorAll('.info-button');
