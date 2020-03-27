export default function convertDate(flaskDate) {
  return flaskDate.slice(0, 10).replace(/-/g, "/")
}