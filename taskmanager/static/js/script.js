document.addEventListener('DOMContentLoaded', function () {
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);

    let modal = document.querySelectorAll('.modal');
    M.Modal.init(modal);

    let datepicker = document.querySelectorAll('.datepicker');
    M.Datepicker.init(datepicker, {
      format: 'dd mmmm, yyyy',
      i18n: {
        done: "Select"
      }
    });
    let select = document.querySelectorAll('select');
    M.FormSelect.init(select);
  });