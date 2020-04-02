export default function convertDate(flaskDate) {
  // convert time to AM/PM
  let time = flaskDate.slice(11, 16);
  // convert to number and check if greater than 12
  let hours = +time.slice(0, 2);
  let minutes = +time.slice(3, 5);
  let ending = "AM";
  if (hours > 12) {
    ending = "PM";
    hours -= 12;
  }

  let string = flaskDate.slice(0, 10).replace(/-/g, "/");
  string += ` ${hours}:${minutes.toString().padStart(2, "0")} ${ending}`;

  return string;
}
