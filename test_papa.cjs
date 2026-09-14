const fs = require('fs');

// simulate fetch
fetch('https://docs.google.com/spreadsheets/d/1RdtvJaS0S1jeSNgBoYZ86WzIfvEIKlo8/export?format=csv&gid=1538508115')
  .then(res => res.text())
  .then(csvText => {
      // Simulate Papa.parse basic behavior for headers
      const lines = csvText.split('\n');
      const headers = lines[0].split(',').map(h => h.trim());
      
      const xambLine = lines.find(l => l.includes('XAMBSNOOKER'));
      if(xambLine) {
          const values = xambLine.split(',');
          const row = {};
          headers.forEach((h, i) => {
              row[h] = values[i];
          });
          console.log("XAMBSNOOKER row['INTEIRA']:", row['INTEIRA']);
          console.log("XAMBSNOOKER row['RGB']:", row['RGB']);
          console.log("XAMBSNOOKER row['600']:", row['600']);
      }
  });
