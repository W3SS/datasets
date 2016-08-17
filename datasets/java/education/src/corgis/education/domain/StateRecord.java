package corgis.education.domain;

import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import corgis.education.domain.Data;

/**
 * 
 */
public class StateRecord {
	
    private String state;
    private Data data;
    
    
    /*
     * @return 
     */
    public String getState() {
        return this.state;
    }
    
    
    
    /*
     * @return 
     */
    public Data getData() {
        return this.data;
    }
    
    
    
	
	/**
	 * Creates a string based representation of this StateRecord.
	
	 * @return String
	 */
	public String toString() {
		return "StateRecord[" +state+", "+data+"]";
	}
	
	/**
	 * Internal constructor to create a StateRecord from a  representation.
	 * @param json_data The raw json data that will be parsed.
	 */
    public StateRecord(JSONObject json_data) {
        try {// state
            this.state = (String)json_data.get("state");// data
            this.data = new Data((JSONObject)json_data.get("data"));
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a StateRecord; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a StateRecord; a field had the wrong structure.");
    		e.printStackTrace();
        }
	}	
}