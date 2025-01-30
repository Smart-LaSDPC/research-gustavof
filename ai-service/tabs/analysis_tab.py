import streamlit as st
from src.prometheus_client import PrometheusMetrics
from src.llm_client import get_llm_analysis
from src.config import Config

def render_analysis_tab(config: Config):
    st.write("Analyze NGINX ingress metrics and get recommendations on load balancing.")
    
    metrics_collector = PrometheusMetrics(config)

    if st.button("Collect and Analyze Metrics"):
        with st.spinner("Collecting metrics from Prometheus..."):
            try:
                # Collect current metrics
                metrics_data = metrics_collector.collect_metrics()
                current_metrics = metrics_data["compact"]
                st.success("Metrics collected successfully.")
                
                # Save metrics with timestamp TODO:fix this
                # metrics_collector.(current_metrics)
                # st.info("Metrics saved to database.")

                with st.spinner("Analyzing..."):
                    try:
                        # Get the LLM analysis using current metrics
                        output = get_llm_analysis(current_metrics, config.OPENAI_API_KEY)
                        st.success("Analysis complete.")
                        
                        # Create a full-width container for the analysis
                        st.subheader("Analysis Results")
                        st.markdown("---")  # Add a visual separator
                        st.write(output)
                        
                        # Add some spacing
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Place metrics summary at the bottom in an expander
                        with st.expander("🔍 View Detailed Metrics Summary"):
                            st.json(current_metrics)

                    except Exception as e:
                        st.error(f"Error during analysis: {e}")

            except Exception as e:
                st.error(f"Error collecting metrics: {e}")