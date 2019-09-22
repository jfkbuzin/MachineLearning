package project;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;

import data.ValidationData;

public class DecisionTree {

	String nodeId;
	double gain;
	HashSet<String> paths;
	List<DecisionTree> branches;
	
	
	public DecisionTree() {
	}

	public DecisionTree(String nodeId, double gain, HashSet<String> paths, List<DecisionTree> branches) {
		this.nodeId = nodeId;
		this.gain = gain;
		this.paths = paths;
		this.branches = branches;
	}

	public HashSet<String> getPaths() {
		return paths;
	}

	public void setPaths(HashSet<String> paths) {
		this.paths = paths;
	}

	public double getGain() {
		return gain;
	}

	public void setGain(double gain) {
		this.gain = gain;
	}

	public String getNodeId() {
		return nodeId;
	}

	public void setNodeId(String nodeId) {
		this.nodeId = nodeId;
	}

	public List<DecisionTree> getBranches() {
		return branches;
	}

	public void setBranches(List<DecisionTree> branches) {
		this.branches = branches;
	}

	//1. Escolher um atributo para adicionar à árvore(iniciando pela raiz) - usar algoritmo ID3 - ganho de informação
	public static String selectAtribute(ArrayList<String> classes, DecisionTree decisionTree, ArrayList<ValidationData> validationData) {
		
		List<AttributeGain> gainList = new ArrayList<AttributeGain>();
		//compute entropy
		double dataSetEntropy = ValidationData.computeDataSetEntropy(validationData);
		double entropyAverage;
		
		if(!classes.contains("Tempo")) {
			entropyAverage = ValidationData.computeSubsetEntropy(validationData, "Tempo", "Ensolarado")
					+ ValidationData.computeSubsetEntropy(validationData, "Tempo", "Nublado")
					+ ValidationData.computeSubsetEntropy(validationData, "Tempo", "Chuvoso");
			
			AttributeGain att = new AttributeGain();
			att.setAttribute("Tempo");
			att.setGain(dataSetEntropy - entropyAverage);
			gainList.add(att);
		}

		if(!classes.contains("Temperatura")) {
			entropyAverage = ValidationData.computeSubsetEntropy(validationData, "Temperatura", "Quente")
					+ ValidationData.computeSubsetEntropy(validationData, "Temperatura", "Fria")
					+ ValidationData.computeSubsetEntropy(validationData, "Temperatura", "Amena");
			
			AttributeGain att = new AttributeGain();
			att.setAttribute("Temperatura");
			att.setGain(dataSetEntropy - entropyAverage);
			gainList.add(att);
		}
			
		if(!classes.contains("Umidade")) {
			entropyAverage = ValidationData.computeSubsetEntropy(validationData, "Umidade", "Alta")
					+ ValidationData.computeSubsetEntropy(validationData, "Umidade", "Normal");
			
			AttributeGain att = new AttributeGain();
			att.setAttribute("Umidade");
			att.setGain(dataSetEntropy - entropyAverage);
			gainList.add(att);
		}
		
		if(!classes.contains("Ventoso")) {
			entropyAverage = ValidationData.computeSubsetEntropy(validationData, "Ventoso", "Falso")
					+ ValidationData.computeSubsetEntropy(validationData, "Ventoso", "Verdadeiro");

			AttributeGain att = new AttributeGain();
			att.setAttribute("Ventoso");
			att.setGain(dataSetEntropy - entropyAverage);
			gainList.add(att);
		}
		
		if(!gainList.isEmpty()) {
			AttributeGain selected = gainList.stream().max(Comparator.comparing(v -> v.getGain())).get();
			
			decisionTree.setGain(selected.getGain());
		
			System.out.println("max gain:" + decisionTree.getGain());
			
			if(decisionTree.getGain() == 0) {
				return "purePartition";
			}
			
			classes.add(selected.getAttribute());
			return selected.getAttribute();
			
		}

		return null;

		
	}
	
	
	public static void selectNodeId(ArrayList<String> classes, DecisionTree decisionTree, ArrayList<ValidationData> validationData) {
		decisionTree.setNodeId(selectAtribute(classes,decisionTree,validationData));
	}
	
	//2. Estender a árvore, adicionando uma ramo para cada valor do atributo selecionado existente
	public static void addBranch(DecisionTree decisionTree, ArrayList<ValidationData> validationData) {
		
		HashSet<String> paths = new HashSet<String>();
				
		
		if(decisionTree.getNodeId().equals("Tempo")) {
			for(ValidationData v : validationData) {
				paths.add(v.getTempo());
			}
		}
		if(decisionTree.getNodeId().equals("Temperatura")) {
			for(ValidationData v : validationData) {
				paths.add(v.getTemperatura());
			}
		}
		if(decisionTree.getNodeId().equals("Umidade")) {
			for(ValidationData v : validationData) {
				paths.add(v.getUmidade());
			}
		}
		if(decisionTree.getNodeId().equals("Ventoso")) {
			for(ValidationData v : validationData) {
				paths.add(v.getVentoso());
			}
		}
		
		decisionTree.setPaths(paths);

	}
	
	//3. Dividir os exemplos em partições (uma para cada ramo adicionado), conforme valor do atributo testado
	public static void splitExamples(ArrayList<String> classes, DecisionTree decisionTree, ArrayList<ValidationData> validationData) {
		
		List<DecisionTree> branches = new ArrayList<DecisionTree>();
		
		for(String path : decisionTree.getPaths()) {
			
			ArrayList<ValidationData> newValidationData = subData(decisionTree, path, validationData);
			
			DecisionTree branchDecisionTree = new DecisionTree();
			
			if(newValidationData.size() > 0) {
				
				
				selectNodeId(classes,branchDecisionTree, newValidationData);
				addBranch(branchDecisionTree, newValidationData);
				branches.add(branchDecisionTree);
				
				splitExamples(classes,branchDecisionTree, newValidationData);
				
			} else {
				//select leaf id
				branchDecisionTree.setNodeId(selectLeafId(decisionTree, path, validationData));
				branches.add(branchDecisionTree);
			}
				
		}
		
		if(branches.size() > 0)
			decisionTree.setBranches(branches);
		
	}
	
	public static ArrayList<ValidationData> subData(DecisionTree decisionTree, String path, ArrayList<ValidationData> validationData){
		ArrayList<ValidationData> newValidationData = new ArrayList<ValidationData>();
		
		
		if(decisionTree.getNodeId().equals("Tempo")) {
			
			if(ValidationData.isPurePartition(validationData, "Tempo", path))
				return newValidationData;
			
			for(ValidationData v : validationData) {
				if(v.getTempo().equals(path)) {
					newValidationData.add(v);
				}
			}			
		}
		
		if(decisionTree.getNodeId().equals("Temperatura")) {
			
			if(ValidationData.isPurePartition(validationData, "Temperatura", path))
				return newValidationData;
			
			for(ValidationData v : validationData) {
				if(v.getTemperatura().equals(path)) {
					newValidationData.add(v);
				}
			}			
		}
		
		if(decisionTree.getNodeId().equals("Umidade")) {
			
			if(ValidationData.isPurePartition(validationData, "Umidade", path))
				return newValidationData;
			
			for(ValidationData v : validationData) {
				if(v.getUmidade().equals(path)) {
					newValidationData.add(v);
				}
			}
		}
		if(decisionTree.getNodeId().equals("Ventoso")) {
			
			if(ValidationData.isPurePartition(validationData, "Ventoso", path))
				return newValidationData;
			
			for(ValidationData v : validationData) {
				if(v.getVentoso().equals(path)) {
					newValidationData.add(v);
				}
			}
		}
		
		
		return newValidationData;
	}
	
	
	public static String selectLeafId(DecisionTree decisionTree, String path, ArrayList<ValidationData> validationData) {
		if(decisionTree.getNodeId().equals("Tempo")) {
			for(ValidationData v : validationData) {
				if(v.getTempo().equals(path)) {
					return v.getJoga();
				}
		}
			
		}
		
		if(decisionTree.getNodeId().equals("Temperatura")) {
			for(ValidationData v : validationData) {
				if(v.getTemperatura().equals(path)) {
					return v.getJoga();
				}
		}
			
		}
		if(decisionTree.getNodeId().equals("Umidade")) {
			for(ValidationData v : validationData) {
				if(v.getUmidade().equals(path)) {
					return v.getJoga();
				}
		}
			
		}
		if(decisionTree.getNodeId().equals("Ventoso")) {
			for(ValidationData v : validationData) {
				if(v.getVentoso().equals(path)) {
					return v.getJoga();
				}
		}
	}
	
	//4. Para cada partição de exemplos resultante, repetir passos 1 a 3
	
}
