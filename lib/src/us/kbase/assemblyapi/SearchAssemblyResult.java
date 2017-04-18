
package us.kbase.assemblyapi;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: SearchAssemblyResult</p>
 * <pre>
 * num_found - number of all items found in query search (with 
 *     only part of it returned in "bins" list).
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "query",
    "start",
    "contigs",
    "num_found"
})
public class SearchAssemblyResult {

    @JsonProperty("query")
    private String query;
    @JsonProperty("start")
    private Long start;
    @JsonProperty("contigs")
    private List<AssemblyData> contigs;
    @JsonProperty("num_found")
    private Long numFound;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("query")
    public String getQuery() {
        return query;
    }

    @JsonProperty("query")
    public void setQuery(String query) {
        this.query = query;
    }

    public SearchAssemblyResult withQuery(String query) {
        this.query = query;
        return this;
    }

    @JsonProperty("start")
    public Long getStart() {
        return start;
    }

    @JsonProperty("start")
    public void setStart(Long start) {
        this.start = start;
    }

    public SearchAssemblyResult withStart(Long start) {
        this.start = start;
        return this;
    }

    @JsonProperty("contigs")
    public List<AssemblyData> getContigs() {
        return contigs;
    }

    @JsonProperty("contigs")
    public void setContigs(List<AssemblyData> contigs) {
        this.contigs = contigs;
    }

    public SearchAssemblyResult withContigs(List<AssemblyData> contigs) {
        this.contigs = contigs;
        return this;
    }

    @JsonProperty("num_found")
    public Long getNumFound() {
        return numFound;
    }

    @JsonProperty("num_found")
    public void setNumFound(Long numFound) {
        this.numFound = numFound;
    }

    public SearchAssemblyResult withNumFound(Long numFound) {
        this.numFound = numFound;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((("SearchAssemblyResult"+" [query=")+ query)+", start=")+ start)+", contigs=")+ contigs)+", numFound=")+ numFound)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
