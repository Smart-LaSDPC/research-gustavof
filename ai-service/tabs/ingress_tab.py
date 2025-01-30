import streamlit as st
from src.kubernetes_client import get_ingress_details, parse_ingress_details, update_ingress_load_balancer
from src.config import Config

def render_ingress_tab(config: Config):
    st.write("View and manage Ingress configuration details")


    # Predefined options for ingress and namespace
    ingress_options = ["iot-app-ingress", "other"]
    namespace_options = ["usp-dev", "usp-prod", "other"]

    # Ingress selection
    ingress_selection = st.selectbox("Select ingress name", ingress_options, index=0)
    if ingress_selection == "other":
        ingress_name = st.text_input("Enter custom ingress name")
    else:
        ingress_name = ingress_selection

    # Namespace selection
    namespace_selection = st.selectbox("Select namespace", namespace_options, index=0)
    if namespace_selection == "other":
        namespace = st.text_input("Enter custom namespace")
    else:
        namespace = namespace_selection

    # Automatically fetch ingress details on load
    raw_details = get_ingress_details(ingress_name, namespace)
    if "Error" in raw_details:
        st.error(raw_details)
    else:
        ingress_details = parse_ingress_details(raw_details)
        st.write("")
        st.success("Ingress details fetched successfully.")
        st.write("")
        
        # Create a container for the metrics
        with st.container():
            metrics = {
                "Name": ingress_details['Name'],
                "Namespace": ingress_details['Namespace'],
                "Host": ingress_details['Host'],
                "Load Balancer Type": ingress_details['Load Balancer Type'],
                "Ingress Class": ingress_details['Ingress Class']
            }
            
            if metrics["Load Balancer Type"] and "nginx.ingress.kubernetes.io/load-balance:" in metrics["Load Balancer Type"]:
                metrics["Load Balancer Type"] = metrics["Load Balancer Type"].split(":")[-1].strip()
            
            for label, value in metrics.items():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write(f"**{label}:**")
                with col2:
                    st.write(value or "N/A")

        # After displaying current metrics, add load balancer modification section
        st.write("")
        st.divider()
        st.subheader("Modify Load Balancer Configuration")
        
        # Load balancer type options
        lb_types = [
            "chash",
            "chashsubset",
            "ewma",
            "resty",
            "round_robin",
            "sticky",
            "sticky_balanced",
            "sticky_persistent"
        ]
        
        new_lb_type = st.selectbox(
            "Select new load balancer type",
            lb_types,
            help="Choose the load balancing algorithm to be applied"
        )
        
        if st.button("Update Load Balancer"):
            success, message = update_ingress_load_balancer(ingress_name, namespace, new_lb_type)
            if success:
                st.success("Load balancer type updated successfully")
            else:
                st.error(message)

        if st.button("Refresh Ingress Details"):
            st.rerun()