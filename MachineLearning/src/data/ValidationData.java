package data;

import java.util.ArrayList;

import project.Util;

public class ValidationData {

	enum Attributes {
	    Tempo,
	    Temperatura,
	    Umidade,
	    Ventoso
	}
	
	
	String tempo;
	String temperatura;
	String umidade;
	String ventoso;
	String joga;
	
	public ValidationData(String tempo, String temperatura, String umidade, String ventoso, String joga) {
		this.tempo = tempo;
		this.temperatura = temperatura;
		this.umidade = umidade;
		this.ventoso = ventoso;
		this.joga = joga;
	}
	
	public String getTempo() {
		return tempo;
	}
	public void setTempo(String tempo) {
		this.tempo = tempo;
	}
	public String getTemperatura() {
		return temperatura;
	}
	public void setTemperatura(String temperatura) {
		this.temperatura = temperatura;
	}
	public String getUmidade() {
		return umidade;
	}
	public void setUmidade(String umidade) {
		this.umidade = umidade;
	}
	public String getVentoso() {
		return ventoso;
	}
	public void setVentoso(String ventoso) {
		this.ventoso = ventoso;
	}
	public String getJoga() {
		return joga;
	}
	public void setJoga(String joga) {
		this.joga = joga;
	}
	
	public void printData() {
		System.out.println(getTempo() + "|" + getTemperatura() + "|" + getUmidade()
		+ "|" + getVentoso() + "|" + getJoga());
	}
	
	public static double computeDataSetEntropy(ArrayList<ValidationData> validationData) {
		double exampleSize = validationData.size(); //14
		double yesSize = 0;
		double noSize = 0;
		
		for(ValidationData v : validationData) {
			if(v.getJoga().equals("Sim")) {
				yesSize++;
			} else {
				noSize++;
			}
				
		}
		
		double d1 = yesSize / exampleSize;
		double d2 = noSize / exampleSize;
		
		double info = -d1*Util.log2(d1)-d2*Util.log2(d2);
		
		System.out.println("info:" + info);
		return info;
	}
	

	public static double computeSubsetEntropy(ArrayList<ValidationData> validationData, String attribute, String example) {
		
		double[] sizes = { 0, 0, 0};
		
		setSizes(validationData, attribute, example, sizes);
		
		double d1;
		double d2;
		double info = 0;
		
		if(sizes[1] > 0 && sizes[0] > 0) {
			d1 = sizes[1] / sizes[0];
			info = info - d1*Util.log2(d1);
		}
			
		
		if(sizes[2] > 0 && sizes[0] > 0) {
			d2 = sizes[2] / sizes[0];
			info = info - d2*Util.log2(d2);
		}
		
		System.out.println("info:" + info);
		//passar já o valor para calcular a média
		if(sizes[0] > 0)
			return (sizes[0]/validationData.size())*info;
		
		return 0;
		
	}
	
	public static void setSizes(ArrayList<ValidationData> validationData, String attribute, String example,
			double[] sizes) {
		
		String presentAttribute = null;
		
		for(ValidationData v : validationData) {
			
			Attributes att = Attributes.valueOf(attribute);
			
			switch(att) {
			case Tempo:
				presentAttribute = v.getTempo();
				break;
			case Temperatura:
				presentAttribute = v.getTemperatura();
				break;
			case Umidade:
				presentAttribute = v.getUmidade();
				break;
			case Ventoso:
				presentAttribute = v.getVentoso();
				break;
			
			}
			
			if(presentAttribute.equals(example)) {
				sizes[0]++;
			}
			
			if(presentAttribute.equals(example) && v.getJoga().equals("Sim")) {
				sizes[1]++;
			}
			if(presentAttribute.equals(example) && v.getJoga().equals("Nao")) {
				sizes[2]++;
			}
		}
	}
	
	public static boolean isPurePartition(ArrayList<ValidationData> validationData, String attribute, String example) {
		double[] sizes = { 0, 0, 0};
		
		setSizes(validationData, attribute, example, sizes);
		
		if(sizes[1] > 0 && sizes[2] == 0 || sizes[1] == 0 && sizes[2] > 0 ) {
			//partição pura
			return true;
		}
		
		return false;
	}
}
