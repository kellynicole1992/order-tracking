import pickle
import os.path

OUTPUT_FOLDER = "output"
TRACKINGS_FILE = OUTPUT_FOLDER + "/trackings.pickle"


class TrackingOutput:

  def save_trackings(self, trackings):
    old_trackings = self.get_existing_trackings()
    merged_trackings = self.merge_trackings(old_trackings, trackings)
    self.write_merged(merged_trackings)

  def write_merged(self, merged_trackings):
    if not os.path.exists(OUTPUT_FOLDER):
      os.mkdir(OUTPUT_FOLDER)

    with open(TRACKINGS_FILE, 'wb') as output:
      pickle.dump(merged_trackings, output)

  # Adds each Tracking object to the appropriate group
  # if there isn't already an entry for that tracking number
  def merge_trackings(self, old_trackings, trackings):
    for group, group_trackings in trackings.items():
      if group in old_trackings:
        old_group_trackings = old_trackings[group]
        old_tracking_numbers = set(
            [ogt.tracking_number for ogt in old_group_trackings])
        for new_group_tracking in group_trackings:
          if new_group_tracking.tracking_number not in old_tracking_numbers:
            old_group_trackings.append(new_group_tracking)
        old_trackings[group] = old_group_trackings
      else:
        old_trackings[group] = group_trackings
    return old_trackings

  def get_existing_trackings(self):
    if not os.path.exists(TRACKINGS_FILE):
      return {}

    with open(TRACKINGS_FILE, 'rb') as tracking_file_stream:
      return pickle.load(tracking_file_stream)

  def clear(self):
    # self.write_merged([])
    pass
