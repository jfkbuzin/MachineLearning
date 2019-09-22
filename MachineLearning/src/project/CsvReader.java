package project;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;

import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;

import data.ValidationData;

public class CsvReader {

	public static File openFile() {
        JFileChooser chooser = new JFileChooser();
        FileNameExtensionFilter filter = new FileNameExtensionFilter(
                "CSV files", "csv");
        chooser.setFileFilter(filter);
        int returnVal = chooser.showOpenDialog(null);
        if(returnVal == JFileChooser.APPROVE_OPTION) {
            System.out.println("You chose to open this file: " +
                    chooser.getSelectedFile().getName());
            File selectedFile = chooser.getSelectedFile();
            return selectedFile;

        }
        return null;
	}
	
	public static void readFile(File csvFile, ArrayList<ValidationData> validationData) {

		if (csvFile.isFile()) {
		    
			BufferedReader csvReader;
			try {
				csvReader = new BufferedReader(new FileReader(csvFile.getAbsolutePath()));
				
				String row;
				
				while ((row = csvReader.readLine()) != null) {
				    String[] data = row.split(",");
				    // print cada linha da tabela
				    for (String d : data) {
				    	
				    	String[] line = d.split(";");
				    	if(!line[0].equals("Tempo")) {
					    	ValidationData vData = new ValidationData(line[0],line[1],line[2],line[3],line[4]);
					    
					    	validationData.add(vData);
				    	}

				    }
				}

				csvReader.close();
				
			} catch (Exception e){
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		}
	}

}
