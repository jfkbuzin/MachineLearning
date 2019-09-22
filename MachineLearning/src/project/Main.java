package project;

import java.io.File;
import java.util.ArrayList;

import data.ValidationData;

public class Main {

	public static void main(String[] args) {

		ArrayList<ValidationData> validationData = new ArrayList<ValidationData>();
		
		File selectedFile = CsvReader.openFile();
		
		CsvReader.readFile(selectedFile,validationData);
		
		for(ValidationData v : validationData) {
			v.printData();
		}
		
		ArrayList<String> classes = new ArrayList<String>();
		
		DecisionTree decisionTree = new DecisionTree();
		DecisionTree.selectNodeId(classes, decisionTree, validationData);
		DecisionTree.addBranch(decisionTree, validationData);
		DecisionTree.splitExamples(classes, decisionTree, validationData);
		
		System.out.println("root attribute selected:" + decisionTree.getNodeId());
	}

}
