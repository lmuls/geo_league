export function formatDate(string: string) {
    if (string) {
      return string.split("T")[0].split("-").reverse().join(".");
    } else {
      return string;
    }
  }