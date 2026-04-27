# Reflection

This project taught me how important human review is especially for a scheduler because it's very likely that the time may not work for the user. It's important for them to be editable. It also showed me that as an engineer, I must not blindly follow AI suggestion, instead carefully read and test their outputs to ensure that it's doing exactly what I want and asks.

## What are the limitations or biases in your system?

Since I focus on understanding RAG system, the knowledge base is limited and it mainly works best with common breeds. If you have other non-generic pets, it usually falls back to general species advice. It also most likely will lean towards certain grooming or execise routines because that may not fit every pet's specific needs. Another limitation is that nothing is saved between sessions. If you refresh or come back later, the system doesn't remember anything about your pet or preferences.

## Could your AI be misused, and how would you prevent that?

Adding too many tasks without reviewing them, leading to an overloaded or conflicting schedule but there's a conflict detection already addressing this. Also, not reviewing time or schedule that AI generated, I made those editable so user can change the time if the schedule doesn't work for them.

## What surprised you while testing your AI's reliability?

The most surprising issue was how error messages from failed API calls were basically vanishing. The app was calling st.rerun() even when something went wrong, which immediately refreshed the page and cleared the error before anyone could see it. Once st.rerun() was moved inside the try block so it only runs after a successful call, the errors finally showed up properly. After that, debugging became a lot more straightforward.

## describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.

One helpful suggestion was combining the "Recurring" and "Every N days" columns into a single readable text column that displays values like "Yes, daily", "Yes, weekly", or "Yes, every 14 days". This made the table cleaner and easier to read, and the text format allowed users to edit the number directly without needing a separate input field.

One flawed suggestion AI gave me was that the table for AI Generated Task was un-editable and each task could not be manually chosen by user.
