export function getBase64FromFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result); // 정상적으로 처리되었을 때
      reader.onerror = error => reject(error);  // 에러 처리
    });
  }