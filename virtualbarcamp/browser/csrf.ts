const csrfToken = (function () {
  const cookieName = "csrftoken";
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(`${cookieName}=`)) {
        return decodeURIComponent(cookie.substring(cookieName.length + 1));
      }
    }
  }
})();

export default csrfToken;
