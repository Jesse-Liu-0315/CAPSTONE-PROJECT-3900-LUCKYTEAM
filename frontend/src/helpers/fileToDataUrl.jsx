// Covert image file to data url
const fileToDataUrl = (file) => {
  // Valid type of image
  const validFileTypes = ['image/jpeg', 'image/png', 'image/jpg'];
  // Check image type
  const valid = validFileTypes.find(type => type === file.type);
  // Bad data, let's walk away.
  if (!valid) {
    throw Error('provided file is not a png, jpg or jpeg image.');
  }

  // Create a new file reader
  const reader = new FileReader();
  // Create a new data url promise
  const dataUrlPromise = new Promise((resolve, reject) => {
    reader.onerror = reject;
    reader.onload = () => resolve(reader.result);
  });
  // Read the file
  reader.readAsDataURL(file);

  return dataUrlPromise;
}

export default fileToDataUrl;
