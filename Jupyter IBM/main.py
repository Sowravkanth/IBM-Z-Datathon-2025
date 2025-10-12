import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import os

# Import custom modules
from utils.data_processor import DataProcessor
from utils.recommendation_engine import RecommendationEngine
from utils.gemini_integration import GeminiIntegration
from utils.market_insights import MarketInsights
from utils.database import Database
from utils.resume_builder import ResumeBuilder
from utils.email_notifications import EmailNotifications
from data.sample_jobs import get_sample_jobs

# Configure page
st.set_page_config(
    page_title="CareerSight AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db = Database()

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'jobs_data' not in st.session_state:
    st.session_state.jobs_data = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'applications' not in st.session_state:
    st.session_state.applications = []

# Initialize components
@st.cache_data
def load_data():
    """Load and process job data"""
    processor = DataProcessor()
    jobs_data = get_sample_jobs()
    processed_data = processor.process_jobs(jobs_data)
    return processed_data

@st.cache_data
def get_market_insights_data(jobs_df):
    """Generate market insights"""
    insights = MarketInsights(jobs_df)
    return insights.generate_insights()

# Load data
if st.session_state.jobs_data is None:
    with st.spinner("Loading job market data..."):
        st.session_state.jobs_data = load_data()

jobs_df = st.session_state.jobs_data

# Initialize engines
recommendation_engine = RecommendationEngine(jobs_df)
gemini_integration = GeminiIntegration()
resume_builder = ResumeBuilder()
email_notifications = EmailNotifications()

# Sidebar Navigation
st.sidebar.title("🎯 CareerSight AI")
st.sidebar.markdown("AI-Powered Career Intelligence")

# User Authentication
st.sidebar.markdown("---")
if st.session_state.user_id is None:
    st.sidebar.subheader("👤 Login")
    with st.sidebar.form("login_form"):
        user_id_input = st.text_input("Enter your User ID", placeholder="e.g., john.doe")
        login_btn = st.form_submit_button("Login")
        
        if login_btn and user_id_input:
            st.session_state.user_id = user_id_input
            # Load user profile from database if available
            if db.is_available():
                try:
                    profile = db.get_user_profile(user_id_input)
                    if profile:
                        st.session_state.user_profile = profile
                        st.sidebar.success(f"Welcome back, {user_id_input}!")
                    else:
                        st.session_state.user_profile = {}
                        st.sidebar.info(f"New user! Please set up your profile.")
                except Exception as e:
                    st.sidebar.warning(f"Could not load profile: {e}")
                    st.session_state.user_profile = {}
            else:
                st.session_state.user_profile = {}
                st.sidebar.warning("Database not available - profile won't be persisted")
            st.rerun()
else:
    st.sidebar.success(f"👤 Logged in as: **{st.session_state.user_id}**")
    if st.sidebar.button("Logout"):
        st.session_state.user_id = None
        st.session_state.user_profile = {}
        st.session_state.applications = []
        st.rerun()

st.sidebar.markdown("---")

menu_options = [
    "📝 Profile Setup",
    "🎯 Job Recommendations", 
    "📚 Learning Roadmap",
    "📊 Skills Gap Analysis",
    "📈 Market Insights",
    "📋 My Applications",
    "🔖 Saved Searches",
    "📄 Resume Builder",
    "🤖 AI Career Coach"
]

selected_option = st.sidebar.radio("Navigate", menu_options)

# Main content area
if selected_option == "📝 Profile Setup":
    st.title("Create Your Career Profile")
    st.markdown("Tell us about your skills, experience, and career goals to get personalized recommendations.")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            skills_input = st.text_area(
                "Skills (comma-separated)",
                value=st.session_state.user_profile.get('skills', ''),
                help="Enter your technical and soft skills separated by commas",
                height=100
            )
            
            experience_level = st.selectbox(
                "Experience Level",
                ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior Level (6-10 years)", "Expert Level (10+ years)"],
                index=0 if not st.session_state.user_profile.get('experience_level') else 
                      ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior Level (6-10 years)", "Expert Level (10+ years)"].index(st.session_state.user_profile.get('experience_level'))
            )
            
            interests = st.text_area(
                "Career Interests",
                value=st.session_state.user_profile.get('interests', ''),
                help="Describe your career interests and goals",
                height=80
            )
        
        with col2:
            location = st.selectbox(
                "Preferred Location",
                ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune", "Chennai", "Kolkata", "Remote", "Any"],
                index=0 if not st.session_state.user_profile.get('location') else
                      ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune", "Chennai", "Kolkata", "Remote", "Any"].index(st.session_state.user_profile.get('location', 'Bangalore'))
            )
            
            salary_min, salary_max = st.slider(
                "Expected Salary Range (LPA)",
                min_value=0,
                max_value=100,
                value=(
                    st.session_state.user_profile.get('salary_min', 5),
                    st.session_state.user_profile.get('salary_max', 20)
                ),
                step=1
            )
            
            industry = st.selectbox(
                "Target Industry",
                ["Technology", "Finance", "Healthcare", "E-commerce", "Consulting", "Manufacturing", "Any"],
                index=0 if not st.session_state.user_profile.get('industry') else
                      ["Technology", "Finance", "Healthcare", "E-commerce", "Consulting", "Manufacturing", "Any"].index(st.session_state.user_profile.get('industry', 'Technology'))
            )
        
        submitted = st.form_submit_button("Save Profile", type="primary")
        
        if submitted:
            if st.session_state.user_id is None:
                st.error("⚠️ Please login first to save your profile!")
            else:
                st.session_state.user_profile = {
                    'skills': skills_input,
                    'experience_level': experience_level,
                    'interests': interests,
                    'location': location,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'industry': industry
                }
                # Save to database if available
                if db.is_available():
                    try:
                        db.save_user_profile(st.session_state.user_id, st.session_state.user_profile)
                        st.success("✅ Profile saved successfully to database!")
                    except Exception as e:
                        st.warning(f"Profile saved in session but could not persist to database: {e}")
                else:
                    st.warning("⚠️ Profile saved in session only (database not available)")
                st.rerun()

    if st.session_state.user_profile:
        st.markdown("---")
        st.subheader("Your Profile Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Skills Count", len([s.strip() for s in st.session_state.user_profile.get('skills', '').split(',') if s.strip()]))
        with col2:
            st.metric("Experience Level", st.session_state.user_profile.get('experience_level', 'Not Set'))
        with col3:
            st.metric("Target Location", st.session_state.user_profile.get('location', 'Not Set'))
        
        # Email Notification Preferences
        if st.session_state.user_id:
            st.markdown("---")
            st.subheader("📧 Email Notification Preferences")
            
            # Load current preferences
            email_prefs = None
            if db.is_available():
                try:
                    email_prefs = db.get_email_preferences(st.session_state.user_id)
                except:
                    pass
            
            with st.form("email_preferences_form"):
                email_input = st.text_input(
                    "Email Address",
                    value=email_prefs.get('email', '') if email_prefs else '',
                    placeholder="your.email@example.com"
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    job_alerts = st.checkbox(
                        "Job Match Alerts",
                        value=email_prefs.get('job_alerts', True) if email_prefs else True,
                        help="Get notified when new jobs match your profile"
                    )
                with col2:
                    roadmap_reminders = st.checkbox(
                        "Learning Reminders",
                        value=email_prefs.get('roadmap_reminders', True) if email_prefs else True,
                        help="Receive reminders for your learning roadmap milestones"
                    )
                with col3:
                    weekly_digest = st.checkbox(
                        "Weekly Digest",
                        value=email_prefs.get('weekly_digest', True) if email_prefs else True,
                        help="Get a weekly summary of job market insights"
                    )
                
                if st.form_submit_button("Save Notification Preferences"):
                    if email_input:
                        preferences = {
                            'job_alerts': job_alerts,
                            'roadmap_reminders': roadmap_reminders,
                            'weekly_digest': weekly_digest
                        }
                        if db.is_available():
                            try:
                                db.save_email_preferences(st.session_state.user_id, email_input, preferences)
                                st.success("✅ Email preferences saved!")
                            except Exception as e:
                                st.error(f"Failed to save preferences: {e}")
                        else:
                            st.warning("Database not available - cannot save preferences")
                        st.rerun()
                    else:
                        st.error("Please enter your email address")

elif selected_option == "🎯 Job Recommendations":
    st.title("Personalized Job Recommendations")
    
    if not st.session_state.user_profile.get('skills'):
        st.warning("⚠️ Please complete your profile setup first to get personalized recommendations.")
        if st.button("Go to Profile Setup"):
            st.rerun()
    else:
        with st.spinner("Finding the best job matches for you..."):
            user_skills = [s.strip() for s in st.session_state.user_profile['skills'].split(',') if s.strip()]
            recommendations = recommendation_engine.get_recommendations(
                user_skills=user_skills,
                location=st.session_state.user_profile.get('location'),
                experience_level=st.session_state.user_profile.get('experience_level'),
                salary_min=st.session_state.user_profile.get('salary_min'),
                salary_max=st.session_state.user_profile.get('salary_max'),
                top_n=10
            )
            
            st.session_state.recommendations = recommendations
        
        if recommendations.empty:
            st.info("No matching jobs found. Try adjusting your profile criteria.")
        else:
            st.success(f"Found {len(recommendations)} job recommendations for you!")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                company_filter = st.selectbox(
                    "Filter by Company",
                    ["All"] + sorted(recommendations['company'].unique().tolist())
                )
            with col2:
                location_filter = st.selectbox(
                    "Filter by Location", 
                    ["All"] + sorted(recommendations['location'].unique().tolist())
                )
            with col3:
                min_score = st.slider("Minimum Compatibility Score", 0.0, 1.0, 0.0, 0.1)
            
            # Apply filters
            filtered_recs = recommendations.copy()
            if company_filter != "All":
                filtered_recs = filtered_recs[filtered_recs['company'] == company_filter]
            if location_filter != "All":
                filtered_recs = filtered_recs[filtered_recs['location'] == location_filter]
            filtered_recs = filtered_recs[filtered_recs['compatibility_score'] >= min_score]
            
            # Display recommendations
            for idx, job in filtered_recs.head(10).iterrows():
                with st.container():
                    st.markdown("---")
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### {job['job_title']}")
                        st.markdown(f"**{job['company']}** • {job['location']}")
                        
                        if pd.notna(job['salary_min']) and pd.notna(job['salary_max']):
                            st.markdown(f"💰 ₹{job['salary_min']:.1f}L - ₹{job['salary_max']:.1f}L per annum")
                        
                        if pd.notna(job['skills']):
                            st.markdown(f"🔧 **Required Skills:** {job['skills']}")
                    
                    with col2:
                        score = job['compatibility_score']
                        st.metric("Compatibility", f"{score:.1%}")
                        
                        if score >= 0.8:
                            st.success("Excellent Match!")
                        elif score >= 0.6:
                            st.info("Good Match")
                        else:
                            st.warning("Partial Match")
                        
                        # Apply button
                        if st.session_state.user_id:
                            if st.button(f"Apply", key=f"apply_{idx}"):
                                job_data = {
                                    'job_title': job['job_title'],
                                    'company': job['company'],
                                    'location': job['location'],
                                    'salary_min': job.get('salary_min'),
                                    'salary_max': job.get('salary_max'),
                                    'skills': job.get('skills', ''),
                                    'status': 'Applied'
                                }
                                if db.is_available():
                                    try:
                                        db.save_job_application(st.session_state.user_id, job_data)
                                        st.success("✅ Application saved!")
                                    except Exception as e:
                                        st.error(f"Failed to save application: {e}")
                                else:
                                    st.warning("Database not available - cannot save application")
                                time.sleep(1)
                                st.rerun()

elif selected_option == "📚 Learning Roadmap":
    st.title("AI-Generated Learning Roadmap")
    
    if not st.session_state.user_profile.get('skills'):
        st.warning("⚠️ Please complete your profile setup first to generate a learning roadmap.")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            target_role = st.text_input(
                "Target Job Role",
                value="Software Engineer",
                help="Enter the job role you're aiming for"
            )
        
        with col2:
            if st.button("Generate Roadmap", type="primary"):
                with st.spinner("Generating personalized learning roadmap..."):
                    user_skills = [s.strip() for s in st.session_state.user_profile['skills'].split(',') if s.strip()]
                    
                    # Get skill gaps
                    skill_gaps = recommendation_engine.analyze_skill_gaps(user_skills, target_role)
                    missing_skills = skill_gaps['missing_skills'][:5]  # Top 5 missing skills
                    
                    # Generate roadmap using Gemini
                    roadmap = gemini_integration.generate_learning_roadmap(
                        target_role=target_role,
                        current_skills=user_skills,
                        missing_skills=missing_skills
                    )
                    
                    if roadmap:
                        st.session_state.current_roadmap = roadmap
        
        if 'current_roadmap' in st.session_state and st.session_state.current_roadmap:
            st.markdown("---")
            st.subheader(f"3-Month Learning Roadmap for {target_role}")
            st.markdown(st.session_state.current_roadmap)
            
            # Add progress tracking
            st.markdown("---")
            st.subheader("Track Your Progress")
            
            weeks = [f"Week {i}" for i in range(1, 13)]
            progress = st.multiselect(
                "Mark completed weeks:",
                weeks,
                default=st.session_state.get('completed_weeks', [])
            )
            st.session_state.completed_weeks = progress
            
            if progress:
                progress_percent = len(progress) / 12 * 100
                st.progress(progress_percent / 100)
                st.success(f"You've completed {progress_percent:.1f}% of your learning roadmap!")

elif selected_option == "📊 Skills Gap Analysis":
    st.title("Skills Gap Analysis")
    
    if not st.session_state.user_profile.get('skills'):
        st.warning("⚠️ Please complete your profile setup first to analyze skill gaps.")
    else:
        user_skills = [s.strip() for s in st.session_state.user_profile['skills'].split(',') if s.strip()]
        
        col1, col2 = st.columns([2, 1])
        with col1:
            target_role = st.text_input("Analyze gaps for role:", value="Software Engineer")
        with col2:
            if st.button("Analyze Skills", type="primary"):
                with st.spinner("Analyzing skill gaps..."):
                    analysis = recommendation_engine.analyze_skill_gaps(user_skills, target_role)
                    st.session_state.skill_analysis = analysis
        
        if 'skill_analysis' in st.session_state:
            analysis = st.session_state.skill_analysis
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Your Current Skills")
                if analysis['existing_skills']:
                    for skill in analysis['existing_skills']:
                        st.success(f"✅ {skill}")
                else:
                    st.info("No matching skills found for this role")
            
            with col2:
                st.subheader("Skills to Develop")
                if analysis['missing_skills']:
                    for i, skill in enumerate(analysis['missing_skills'][:10], 1):
                        priority = "🔴 High" if i <= 3 else "🟡 Medium" if i <= 6 else "🟢 Low"
                        st.markdown(f"{priority} Priority: **{skill}**")
                else:
                    st.success("You have all the required skills!")
            
            # Skills comparison chart
            if analysis['missing_skills'] or analysis['existing_skills']:
                st.markdown("---")
                st.subheader("Skills Overview")
                
                existing_count = len(analysis['existing_skills'])
                missing_count = len(analysis['missing_skills'][:10])
                
                fig = go.Figure(data=[
                    go.Bar(name='You Have', x=['Skills'], y=[existing_count], marker_color='green'),
                    go.Bar(name='Need to Learn', x=['Skills'], y=[missing_count], marker_color='orange')
                ])
                fig.update_layout(barmode='stack', title="Skills Gap Overview")
                st.plotly_chart(fig, use_container_width=True)

elif selected_option == "📈 Market Insights":
    st.title("Real-Time Market Intelligence")
    
    with st.spinner("Analyzing job market trends..."):
        insights = get_market_insights_data(jobs_df)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Jobs", f"{len(jobs_df):,}")
    with col2:
        avg_salary = jobs_df['salary_max'].mean() if 'salary_max' in jobs_df.columns else 0
        st.metric("Avg. Max Salary", f"₹{avg_salary:.1f}L")
    with col3:
        st.metric("Top Location", insights['top_locations'][0]['location'] if insights['top_locations'] else "N/A")
    with col4:
        st.metric("Top Skill", insights['top_skills'][0]['skill'] if insights['top_skills'] else "N/A")
    
    st.markdown("---")
    
    # Visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Top Companies", "📍 Job Locations", "💼 In-Demand Skills", "💰 Salary Trends"])
    
    with tab1:
        st.subheader("Top Hiring Companies")
        if insights['top_companies']:
            companies_df = pd.DataFrame(insights['top_companies'])
            fig = px.bar(companies_df, x='count', y='company', orientation='h',
                        title="Companies with Most Job Openings")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Job Distribution by Location")
        if insights['top_locations']:
            locations_df = pd.DataFrame(insights['top_locations'])
            fig = px.pie(locations_df, values='count', names='location',
                        title="Job Distribution Across Cities")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Most In-Demand Skills")
        if insights['top_skills']:
            skills_df = pd.DataFrame(insights['top_skills'][:15])
            fig = px.bar(skills_df, x='count', y='skill', orientation='h',
                        title="Skills in Highest Demand")
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Salary Trends by Experience Level")
        if 'experience_level' in jobs_df.columns and 'salary_max' in jobs_df.columns:
            salary_trends = jobs_df.groupby('experience_level')['salary_max'].mean().reset_index()
            fig = px.line(salary_trends, x='experience_level', y='salary_max',
                         title="Average Maximum Salary by Experience Level",
                         markers=True)
            st.plotly_chart(fig, use_container_width=True)

elif selected_option == "📋 My Applications":
    st.title("Job Application Tracker")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Please login to track your job applications.")
    else:
        # Load applications from database
        applications = []
        if db.is_available():
            try:
                applications = db.get_user_applications(st.session_state.user_id)
            except Exception as e:
                st.error(f"Failed to load applications: {e}")
        else:
            st.warning("Database not available - cannot load applications")
        
        if not applications:
            st.info("📝 You haven't applied to any jobs yet. Start browsing job recommendations!")
        else:
            st.success(f"You have {len(applications)} job application(s)")
            
            # Filter by status
            col1, col2 = st.columns([2, 1])
            with col1:
                status_filter = st.selectbox(
                    "Filter by Status",
                    ["All", "Applied", "Interview", "Offered", "Rejected", "Accepted"]
                )
            
            # Display applications
            for app in applications:
                if status_filter == "All" or app['status'] == status_filter:
                    with st.expander(f"{app['job_title']} at {app['company']} - {app['status']}"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Company:** {app['company']}")
                            st.markdown(f"**Location:** {app['location']}")
                            if app.get('salary_min') and app.get('salary_max'):
                                st.markdown(f"**Salary:** ₹{app['salary_min']:.1f}L - ₹{app['salary_max']:.1f}L")
                            st.markdown(f"**Applied:** {app['applied_date'].strftime('%Y-%m-%d %H:%M')}")
                            if app.get('skills'):
                                st.markdown(f"**Skills:** {app['skills']}")
                        
                        with col2:
                            st.markdown(f"**Current Status:** {app['status']}")
                            
                            # Update status
                            new_status = st.selectbox(
                                "Update Status",
                                ["Applied", "Interview", "Offered", "Rejected", "Accepted"],
                                index=["Applied", "Interview", "Offered", "Rejected", "Accepted"].index(app['status']),
                                key=f"status_{app['id']}"
                            )
                            
                            notes = st.text_area(
                                "Notes",
                                value=app.get('notes', ''),
                                key=f"notes_{app['id']}",
                                height=80
                            )
                            
                            if st.button("Update", key=f"update_{app['id']}"):
                                db.update_application_status(app['id'], new_status, notes)
                                st.success("✅ Application updated!")
                                time.sleep(1)
                                st.rerun()

elif selected_option == "🔖 Saved Searches":
    st.title("Saved Job Searches")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Please login to save your job searches.")
    else:
        # Save current search
        st.subheader("Save Current Search Filters")
        
        with st.form("save_search_form"):
            search_name = st.text_input("Search Name", placeholder="e.g., Senior Python Developer in Bangalore")
            
            col1, col2 = st.columns(2)
            with col1:
                search_location = st.selectbox(
                    "Location",
                    ["Any", "Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune", "Chennai", "Remote"]
                )
                search_exp_level = st.selectbox(
                    "Experience Level",
                    ["Any", "Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior Level (6-10 years)", "Expert Level (10+ years)"]
                )
            
            with col2:
                search_salary_min = st.number_input("Min Salary (LPA)", min_value=0, max_value=100, value=5)
                search_salary_max = st.number_input("Max Salary (LPA)", min_value=0, max_value=100, value=25)
            
            if st.form_submit_button("Save Search"):
                if search_name:
                    filters = {
                        'location': search_location,
                        'experience_level': search_exp_level,
                        'salary_min': search_salary_min,
                        'salary_max': search_salary_max
                    }
                    db.save_search(st.session_state.user_id, search_name, filters)
                    st.success(f"✅ Search '{search_name}' saved!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Please enter a search name")
        
        # Display saved searches
        st.markdown("---")
        st.subheader("Your Saved Searches")
        
        saved_searches = db.get_user_searches(st.session_state.user_id)
        
        if not saved_searches:
            st.info("💾 No saved searches yet. Save your first search above!")
        else:
            for search in saved_searches:
                with st.expander(f"🔍 {search['search_name']}"):
                    filters = search['filters']
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Location:** {filters.get('location', 'Any')}")
                        st.markdown(f"**Experience:** {filters.get('experience_level', 'Any')}")
                        st.markdown(f"**Salary Range:** ₹{filters.get('salary_min', 0)}L - ₹{filters.get('salary_max', 0)}L")
                        st.markdown(f"**Created:** {search['created_at'].strftime('%Y-%m-%d')}")
                    
                    with col2:
                        if st.button("Delete", key=f"delete_{search['id']}"):
                            db.delete_search(search['id'])
                            st.success("Deleted!")
                            time.sleep(1)
                            st.rerun()

elif selected_option == "📄 Resume Builder":
    st.title("AI-Powered Resume Builder")
    st.markdown("Create a professional resume with AI-powered optimization and export to PDF")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Please login to use the resume builder.")
    else:
        # Initialize resume data in session state
        if 'resume_data' not in st.session_state:
            st.session_state.resume_data = resume_builder.create_sample_resume(st.session_state.user_profile)
        
        tabs = st.tabs(["📝 Basic Info", "💼 Experience", "🎓 Education", "🚀 Projects", "🏆 Certifications", "📥 Export"])
        
        # Tab 1: Basic Information
        with tabs[0]:
            st.subheader("Basic Information")
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name", value=st.session_state.resume_data.get('name', ''))
                email = st.text_input("Email", value=st.session_state.resume_data.get('email', ''))
                phone = st.text_input("Phone", value=st.session_state.resume_data.get('phone', ''))
            
            with col2:
                location = st.text_input("Location", value=st.session_state.resume_data.get('location', ''))
                linkedin = st.text_input("LinkedIn", value=st.session_state.resume_data.get('linkedin', ''))
            
            summary = st.text_area(
                "Professional Summary",
                value=st.session_state.resume_data.get('summary', ''),
                height=100,
                help="Brief overview of your professional background"
            )
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🤖 Optimize Summary", key="optimize_summary"):
                    with st.spinner("Optimizing..."):
                        optimized = gemini_integration.optimize_resume_content(
                            "professional summary",
                            summary,
                            st.session_state.user_profile.get('interests', '')
                        )
                        st.session_state.resume_data['summary'] = optimized
                        st.success("✅ Summary optimized!")
                        st.rerun()
            
            skills = st.text_area(
                "Skills",
                value=st.session_state.resume_data.get('skills', ''),
                height=80,
                help="List your technical and soft skills"
            )
            
            if st.button("Save Basic Info", type="primary"):
                st.session_state.resume_data.update({
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'location': location,
                    'linkedin': linkedin,
                    'summary': summary,
                    'skills': skills
                })
                st.success("✅ Basic info saved!")
        
        # Tab 2: Experience
        with tabs[1]:
            st.subheader("Work Experience")
            
            if 'experience' not in st.session_state.resume_data:
                st.session_state.resume_data['experience'] = []
            
            # Add new experience
            with st.expander("➕ Add New Experience", expanded=False):
                exp_title = st.text_input("Job Title", key="new_exp_title")
                exp_company = st.text_input("Company", key="new_exp_company")
                exp_duration = st.text_input("Duration", placeholder="e.g., Jan 2020 - Present", key="new_exp_duration")
                exp_desc = st.text_area("Description & Achievements", key="new_exp_desc", height=100)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Add Experience"):
                        if exp_title and exp_company:
                            st.session_state.resume_data['experience'].append({
                                'title': exp_title,
                                'company': exp_company,
                                'duration': exp_duration,
                                'description': exp_desc
                            })
                            st.success("✅ Experience added!")
                            st.rerun()
                with col2:
                    if st.button("🤖 Optimize Description", key="optimize_new_exp"):
                        if exp_desc:
                            optimized = gemini_integration.optimize_resume_content(
                                "work experience",
                                exp_desc,
                                exp_title
                            )
                            st.text_area("Optimized Description", value=optimized, height=100)
            
            # Display existing experiences
            for idx, exp in enumerate(st.session_state.resume_data.get('experience', [])):
                with st.expander(f"{exp['title']} at {exp['company']}"):
                    st.markdown(f"**Duration:** {exp.get('duration', 'N/A')}")
                    st.markdown(f"**Description:**\n{exp.get('description', '')}")
                    
                    if st.button("Remove", key=f"remove_exp_{idx}"):
                        st.session_state.resume_data['experience'].pop(idx)
                        st.rerun()
        
        # Tab 3: Education
        with tabs[2]:
            st.subheader("Education")
            
            if 'education' not in st.session_state.resume_data:
                st.session_state.resume_data['education'] = []
            
            with st.expander("➕ Add Education", expanded=False):
                edu_degree = st.text_input("Degree", key="new_edu_degree")
                edu_institution = st.text_input("Institution", key="new_edu_institution")
                edu_year = st.text_input("Year/Duration", key="new_edu_year")
                edu_details = st.text_area("Details (GPA, achievements, etc.)", key="new_edu_details")
                
                if st.button("Add Education"):
                    if edu_degree and edu_institution:
                        st.session_state.resume_data['education'].append({
                            'degree': edu_degree,
                            'institution': edu_institution,
                            'year': edu_year,
                            'details': edu_details
                        })
                        st.success("✅ Education added!")
                        st.rerun()
            
            for idx, edu in enumerate(st.session_state.resume_data.get('education', [])):
                with st.expander(f"{edu['degree']} - {edu['institution']}"):
                    st.markdown(f"**Year:** {edu.get('year', 'N/A')}")
                    st.markdown(f"**Details:** {edu.get('details', '')}")
                    
                    if st.button("Remove", key=f"remove_edu_{idx}"):
                        st.session_state.resume_data['education'].pop(idx)
                        st.rerun()
        
        # Tab 4: Projects
        with tabs[3]:
            st.subheader("Projects")
            
            if 'projects' not in st.session_state.resume_data:
                st.session_state.resume_data['projects'] = []
            
            with st.expander("➕ Add Project", expanded=False):
                proj_name = st.text_input("Project Name", key="new_proj_name")
                proj_duration = st.text_input("Duration/Year", key="new_proj_duration")
                proj_desc = st.text_area("Description", key="new_proj_desc")
                
                if st.button("Add Project"):
                    if proj_name:
                        st.session_state.resume_data['projects'].append({
                            'name': proj_name,
                            'duration': proj_duration,
                            'description': proj_desc
                        })
                        st.success("✅ Project added!")
                        st.rerun()
            
            for idx, proj in enumerate(st.session_state.resume_data.get('projects', [])):
                with st.expander(f"{proj['name']}"):
                    st.markdown(f"**Duration:** {proj.get('duration', 'N/A')}")
                    st.markdown(f"**Description:** {proj.get('description', '')}")
                    
                    if st.button("Remove", key=f"remove_proj_{idx}"):
                        st.session_state.resume_data['projects'].pop(idx)
                        st.rerun()
        
        # Tab 5: Certifications
        with tabs[4]:
            st.subheader("Certifications")
            
            if 'certifications' not in st.session_state.resume_data:
                st.session_state.resume_data['certifications'] = []
            
            with st.expander("➕ Add Certification", expanded=False):
                cert_name = st.text_input("Certification Name", key="new_cert_name")
                cert_issuer = st.text_input("Issuing Organization", key="new_cert_issuer")
                cert_year = st.text_input("Year", key="new_cert_year")
                
                if st.button("Add Certification"):
                    if cert_name:
                        st.session_state.resume_data['certifications'].append({
                            'name': cert_name,
                            'issuer': cert_issuer,
                            'year': cert_year
                        })
                        st.success("✅ Certification added!")
                        st.rerun()
            
            for idx, cert in enumerate(st.session_state.resume_data.get('certifications', [])):
                with st.expander(f"{cert['name']}"):
                    st.markdown(f"**Issuer:** {cert.get('issuer', 'N/A')}")
                    st.markdown(f"**Year:** {cert.get('year', 'N/A')}")
                    
                    if st.button("Remove", key=f"remove_cert_{idx}"):
                        st.session_state.resume_data['certifications'].pop(idx)
                        st.rerun()
        
        # Tab 6: Export
        with tabs[5]:
            st.subheader("Export Your Resume")
            
            st.info("📄 Your resume is ready! Click the button below to download as PDF.")
            
            # Generate PDF
            if st.button("📥 Download PDF Resume", type="primary"):
                with st.spinner("Generating PDF..."):
                    pdf_buffer = resume_builder.generate_pdf(st.session_state.resume_data)
                    
                    st.download_button(
                        label="💾 Download Resume.pdf",
                        data=pdf_buffer,
                        file_name=f"{st.session_state.resume_data.get('name', 'Resume').replace(' ', '_')}_Resume.pdf",
                        mime="application/pdf"
                    )
                    st.success("✅ Resume generated successfully!")

elif selected_option == "🤖 AI Career Coach":
    st.title("AI-Powered Career Assistant")
    st.markdown("Get personalized career advice, interview tips, and professional guidance.")
    
    # Chat interface
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hello! I'm your AI Career Coach. I can help you with interview preparation, resume advice, career transitions, and professional development. What would you like to discuss today?"}
        ]
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Quick action buttons
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Resume Tips"):
            prompt = "Give me 5 important tips for improving my resume to get more job interviews in the tech industry."
            st.session_state.chat_messages.append({"role": "user", "content": "Resume Tips"})
            
            with st.spinner("Getting resume advice..."):
                response = gemini_integration.get_career_advice(prompt)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("💼 Interview Prep"):
            prompt = "Help me prepare for a software engineering interview. What are the most common questions and how should I approach technical interviews?"
            st.session_state.chat_messages.append({"role": "user", "content": "Interview Preparation"})
            
            with st.spinner("Preparing interview guidance..."):
                response = gemini_integration.get_career_advice(prompt)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("🌐 Networking Tips"):
            prompt = "Give me practical strategies for professional networking and building meaningful connections in my industry."
            st.session_state.chat_messages.append({"role": "user", "content": "Networking Strategies"})
            
            with st.spinner("Getting networking advice..."):
                response = gemini_integration.get_career_advice(prompt)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your career..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Thinking..."):
            # Add user context if profile exists
            context = ""
            if st.session_state.user_profile.get('skills'):
                context = f"User profile: Skills: {st.session_state.user_profile['skills']}, Experience: {st.session_state.user_profile.get('experience_level', 'Not specified')}, Location: {st.session_state.user_profile.get('location', 'Not specified')}. "
            
            full_prompt = context + prompt
            response = gemini_integration.get_career_advice(full_prompt)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        st.rerun()

# Footer
st.markdown("---")
st.markdown("**CareerSight AI** - Powered by Google Gemini | Built with ❤️ for Career Growth")
