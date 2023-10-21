from datetime import timedelta
import random as rand
from faker import Faker
import json
import random

fake = Faker()

# Generate dummy data for a User entity
def generate_user(user_id):
    return {
        "user_id": user_id,
        "username": fake.user_name(),
        "fullname": fake.name(),
        "email": fake.email(),
        "birthdate": fake.date_of_birth().strftime('%Y-%m-%d'),
        "gender": fake.random_element(["Male", "Female", "Other"]),
        "location": fake.city(),
        "relationship_status": fake.random_element(["Single", "In a Relationship", "Married"]),
        "bio": fake.text(),
        "profile_picture": fake.image_url(),
        "join_date": fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S'),
        # Add other attributes
    }


# Generate dummy data for a Post entity
def generate_post(post_id, user_id):
    user_ids = random.sample(range(1, len(user_id)), 1)  # Get 1 random user IDs
    return {
        "post_id": post_id,
        "user_id": user_ids,
        "content": fake.paragraph(),
        "media": fake.random_element([fake.image_url(), fake.url()]),
        "timestamp": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
        "privacy_setting": fake.random_element(["Public", "Friends", "Private"]),
        "is_pinned": fake.boolean()
        # Add other attributes
    }


# Generate dummy data for a Comment entity
def generate_comment(comment_id, post_id, user_id):
    user_ids = random.sample(range(1, len(user_id)), 1)  # Get 1 random user IDs
    post_ids = random.sample(range(1, len(post_id)), 1)  # Get 1 random user IDs
    return {
        "comment_id": comment_id,
        "post_id": post_ids,
        "user_id": user_ids,
        "content": fake.sentence(),
        "timestamp": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        # Add other attributes
    }


# Generate dummy data for a Like entity
def generate_like(like_id, user_id, post_id):
    user_ids = random.sample(range(1, len(user_id)), 1)  # Get 1 random user IDs
    post_ids = random.sample(range(1, len(post_id)), 1)  # Get 1 random user IDs
    return {
        "like_id": like_id,
        "user_id": user_ids,
        "post_id": post_ids,
        "timestamp": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        # Add other attributes
    }


# Generate dummy data for a Share entity
def generate_share(share_id, user_id, post_id):
    user_ids = random.sample(range(1, len(user_id)), 1)  # Get 1 random user IDs
    post_ids = random.sample(range(1, len(post_id)), 1)  # Get 1 random user IDs
    return {
        "share_id": share_id,
        "user_id": user_ids,
        "post_id": post_ids,
        "timestamp": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        # Add other attributes
    }


# Generate dummy data for a FriendRequest entity
def generate_friend_request(request_id, sender_id, receiver_id):
    sender_ids = random.sample(range(1, len(sender_id)), 1)  # Get 1 random user IDs
    receiver_ids = random.sample(range(1, len(receiver_id)), 1)  # Get 1 random user IDs
    return {
        "request_id": request_id,
        "sender_id": sender_ids,
        "receiver_id": receiver_ids,
        "status": fake.random_element(["Pending", "Accepted", "Declined"]),
        "timestamp": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        # Add other attributes
    }


# Generate dummy data for a Message entity
def generate_message(message_id, sender_id, receiver_id):
    sender_ids = random.sample(range(1, len(sender_id)), 1)  # Get 1 random user IDs
    receiver_ids = random.sample(range(1, len(receiver_id)), 1)  # Get 1 random user IDs
    return {
        "message_id": message_id,
        "sender_id": sender_ids,
        "receiver_id": receiver_ids,
        "content": fake.text(),
        "timestamp": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        # Add other attributes
    }


# Generate dummy data for a Group entity
def generate_group(group_id, user_id):
    user_ids = random.sample(range(1, len(user_id)), random.randint(1, 30))  # users in a group
    return {
        "group_id": group_id,
        "user_id": user_ids,
        "name": fake.word(),
        "description": fake.sentence(),
        "creation_date": fake.date_this_decade().strftime('%Y-%m-%d'),
        "privacy_setting": fake.random_element(["Public", "Private"])
        # Add other attributes
    }


# Generate dummy data for a Page entity
def generate_page(page_id):
    return {
        "page_id": page_id,
        "name": fake.word(),
        "description": fake.sentence(),
        "creation_date": fake.date_this_decade().strftime('%Y-%m-%d'),
        "category": fake.random_element(["Entertainment", "Business", "News"])
        # Add other attributes
    }


# Generate dummy data for an Event entity
def generate_event(event_id, user_id):
    user_ids = random.sample(range(1, len(user_id)), 1)  # Get 1 random user IDs
    return {
        "event_id": event_id,
        "user_id": user_ids,
        "name": fake.sentence(),
        "description": fake.paragraph(),
        "start_datetime": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
        "end_datetime": (fake.date_time_this_year() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
        "location": fake.city(),
        "privacy_setting": fake.random_element(["Public", "Friends", "Private"])
        # Add other attributes
    }


# Generate dummy data for a Hashtag entity
def generate_hashtag(hashtag_id):
    return {
        "hashtag_id": hashtag_id,
        "tag": fake.word()
        # Add other attributes
    }


# Generate dummy data for a Notification entity
def generate_notification(notification_id, user_id):
    user_ids = random.sample(range(1, len(user_id)), 1)  # Get 1 random user IDs
    return {
        "notification_id": notification_id,
        "user_id": user_ids,
        "content": fake.sentence(),
        "timestamp": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
        "status": fake.random_element(["Unread", "Read"])
        # Add other attributes
    }


# Generate dummy data for a Poll entity
def generate_poll(poll_id, user_id):
    user_ids = random.sample(range(1, len(user_id)), 1)  # Get 1 random user IDs
    return {
        "poll_id": poll_id,
        "user_id": user_ids,
        "question": fake.sentence(),  # Corrected from fake.question()
        "options_count": fake.random_int(min=2, max=5),
        "expiration_date": (fake.date_time_this_year() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
        "privacy_setting": fake.random_element(["Public", "Friends", "Private"])
        # Add other attributes
    }


# Generate dummy data for a PollOption entity
def generate_poll_option(option_id, poll_id):
    poll_ids = random.sample(range(1, len(poll_id)), 1)  # Get 1 random user IDs
    return {
        "option_id": option_id,
        "poll_id": poll_ids,
        "content": fake.word()
        # Add other attributes
    }


# Generate dummy data for an Album entity
def generate_album(album_id, user_id):
    user_ids = random.sample(range(1, len(user_id)), 1)  # Get 1 random user IDs
    return {
        "album_id": album_id,
        "user_id": user_ids,
        "name": fake.sentence(),
        "description": fake.paragraph(),
        "creation_date": fake.date_this_decade().strftime('%Y-%m-%d')
        # Add other attributes
    }


# Generate dummy data for a Photo entity
def generate_photo(photo_id, album_id, user_id):
    user_ids = random.sample(range(1, len(user_id)), 1)  # Get 1 random user IDs
    album_ids = random.sample(range(1, len(album_id)), 1)  # Get 1 random user IDs
    return {
        "photo_id": photo_id,
        "album_id": album_ids,
        "user_id": user_ids,
        "image_url": fake.image_url(),
        "timestamp": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
        "caption": fake.sentence()
        # Add other attributes
    }


# Generate dummy data for a Video entity
def generate_video(video_id, user_id):
    user_ids = random.sample(range(1, len(user_id)), 1)  # Get 1 random user IDs
    return {
        "video_id": video_id,
        "user_id": user_ids,
        "title": fake.sentence(),
        "description": fake.paragraph(),
        "video_url": fake.url(),
        "timestamp": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        # Add other attributes
    }


# Generate dummy data for multiple entries of each entity
def generate_data(num_entries, entity_generator, *args):
    data = []
    for entry_id in range(1, num_entries + 1):
        entry = entity_generator(entry_id, *args)
        data.append(entry)
    return data



# Generate  dummy  entries
def generate_and_save_data(population):
    print("Generating users...")
    dummy_users = generate_data(population, generate_user)
    with open("largeSocialDBJson/users.json", "w") as json_file:
        json.dump(dummy_users, json_file, indent=4)

    print("Generating posts...")
    dummy_posts = generate_data(population, generate_post, dummy_users)
    with open("largeSocialDBJson/posts.json", "w") as json_file:
        json.dump(dummy_posts, json_file, indent=4)

    print("Generating comments...")
    dummy_comments = generate_data(population, generate_comment, dummy_posts, dummy_users)
    with open("largeSocialDBJson/comments.json", "w") as json_file:
        json.dump(dummy_comments, json_file, indent=4)

    print("Generating friend requests...")
    dummy_friend_requests = generate_data(population, generate_friend_request, dummy_users, dummy_users)
    with open("largeSocialDBJson/friend_requests.json", "w") as json_file:
        json.dump(dummy_friend_requests, json_file, indent=4)

    print("Generating likes...")
    dummy_likes = generate_data(population, generate_like, dummy_users, dummy_posts)
    with open("largeSocialDBJson/likes.json", "w") as json_file:
        json.dump(dummy_likes, json_file, indent=4)

    print("Generating shares...")
    dummy_shares = generate_data(population, generate_share, dummy_users, dummy_posts)
    with open("largeSocialDBJson/shares.json", "w") as json_file:
        json.dump(dummy_shares, json_file, indent=4)

    print("Generating messages...")
    dummy_messages = generate_data(population, generate_message, dummy_users, dummy_users)
    with open("largeSocialDBJson/messages.json", "w") as json_file:
        json.dump(dummy_messages, json_file, indent=4)

    print("Generating groups...")
    dummy_groups = generate_data(population, generate_group, dummy_users)
    with open("largeSocialDBJson/groups.json", "w") as json_file:
        json.dump(dummy_groups, json_file, indent=4)

    print("Generating pages...")
    dummy_pages = generate_data(population, generate_page)
    with open("largeSocialDBJson/pages.json", "w") as json_file:
        json.dump(dummy_pages, json_file, indent=4)

    print("Generating events...")
    # Generate 50 dummy Event entries
    dummy_events = generate_data(population, generate_event, dummy_users)
    with open("largeSocialDBJson/events.json", "w") as json_file:
        json.dump(dummy_events, json_file, indent=4)

    print("Generating hashtags...")
    dummy_hashtags = generate_data(population, generate_hashtag)
    with open("largeSocialDBJson/hashtags.json", "w") as json_file:
        json.dump(dummy_hashtags, json_file, indent=4)

    print("Generating notifications...")
    dummy_notifications = generate_data(population, generate_notification, dummy_users)
    with open("largeSocialDBJson/notifications.json", "w") as json_file:
        json.dump(dummy_notifications, json_file, indent=4)

    print("Generating polls...")
    dummy_polls = generate_data(population, generate_poll, dummy_users)
    with open("largeSocialDBJson/polls.json", "w") as json_file:
        json.dump(dummy_polls, json_file, indent=4)

    print("Generating poll options...")
    dummy_poll_options = generate_data(population, generate_poll_option, dummy_polls)
    with open("largeSocialDBJson/poll_options.json", "w") as json_file:
        json.dump(dummy_poll_options, json_file, indent=4)

    print("Generating albums...")
    dummy_albums = generate_data(population, generate_album, dummy_users)
    with open("largeSocialDBJson/albums.json", "w") as json_file:
        json.dump(dummy_albums, json_file, indent=4)

    print("Generating photos...")
    dummy_photos = generate_data(population, generate_photo, dummy_albums, dummy_users)
    with open("largeSocialDBJson/photos.json", "w") as json_file:
        json.dump(dummy_photos, json_file, indent=4)

    print("Generating videos...")
    dummy_videos = generate_data(population, generate_video, dummy_users)
    with open("largeSocialDBJson/videos.json", "w") as json_file:
        json.dump(dummy_videos, json_file, indent=4)



