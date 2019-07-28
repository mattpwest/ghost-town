### More Elegant Time System 
Featuring these components:
 - Time: `delta` time passed.
 - TimeAffected: Tracks total time or duration remaining.

And these systems:
 - ActionSystem: puts Time on all TimeAffected entities whenever time passes (entities ticked).
 - TimeSystem: applies Time to TimeAffected then deletes Time.
 - TimeEffectsSystem: triggers things when TimeSystem has accumulated enough time.